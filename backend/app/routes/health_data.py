from flask import Blueprint, jsonify, current_app
from app.repositories.user_repo import UserRepository
from app.repositories.run_repo import RunRepository

health_data_bp = Blueprint('health_data', _name_, url_prefix='/health-data')

@health_data_bp.route('/<string:user_id>', methods=['GET'])
def get_user_health_summary(user_id: str):
    current_app.logger.info(f"Received health summary request for user_id: {user_id}")

    user = UserRepository.get_by_id(user_id)
    if not user:
        current_app.logger.warning(f"User with user_id: {user_id} not found for health summary request.")
        return jsonify({"error": "User not found"}), 404
    
    user_name = f"{user.first_name} {user.last_name}"
    user_age = user.age
    user_weight = user.weight_kg
    user_ecg_result = user.ecg_result

    avg_heart_rate = None
    try:
        avg_heart_rate = RunRepository.get_avg_heart_rate_last_15_mins(user_id)
        if avg_heart_rate is not None:
            current_app.logger.info(f"Average heart rate for user {user_id} in last 15 mins: {avg_heart_rate}")
        else:
            current_app.logger.info(f"No heart rate data found for user {user_id} in the last 15 mins.")
    except Exception as e:
        current_app.logger.error(f"Error getting avg heart rate for user {user_id}: {e}", exc_info=True)

    avg_pace = None
    try:
        avg_pace = RunRepository.get_avg_pace_last_15_mins(user_id)
        if avg_pace is not None:
            current_app.logger.info(f"Average pace for user {user_id} in last 15 mins: {avg_pace}")
        else:
            current_app.logger.info(f"No pace data found for user {user_id} in the last 15 mins.")
    except Exception as e:
        current_app.logger.error(f"Error getting avg pace for user {user_id}: {e}", exc_info=True)
    
    response_data = {
        "user_id": user_id,
        "name": user_name,
        "age": user_age,
        "weight_kg": user_weight,
        "ecg_result": user_ecg_result,
        "average_heart_rate_last_15_mins": avg_heart_rate,
        "average_pace_last_15_mins": avg_pace
    }

    return jsonify(response_data), 200
