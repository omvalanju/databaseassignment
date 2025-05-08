from flask import Blueprint, request, jsonify, current_app
from app.models.run import Run
from app.repositories.run_repo import RunRepository

run_bp = Blueprint('run', __name__, url_prefix='/run')

@run_bp.route('', methods=['POST'])
def ingest_run():
    data = request.get_json(force=True)
    missing = [k for k in ('user_id', 'heart_rate', 'pace', 'distance', 'timestamp') if k not in data]
    if missing:
        return jsonify({'error': f"Missing fields: {', '.join(missing)}"}), 400

    try:
        run = Run(
            user_id    = data['user_id'],
            heart_rate = data['heart_rate'],
            pace       = data['pace'],
            distance   = data['distance'],
            timestamp  = data['timestamp']
        )
        RunRepository.insert(run)
        return jsonify({'status': 'ok'}), 200

    except Exception as e:
        current_app.logger.error(f"Error ingesting run: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@run_bp.route('/<string:user_id>', methods=['GET'])
def get_runs(user_id):
    try:
        limit = int(request.args.get('limit', 5))
        runs = RunRepository.get_recent_runs(user_id, limit=limit)
        return jsonify([r.to_dict() for r in runs]), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching runs for {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500
