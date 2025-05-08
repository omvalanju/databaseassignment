from flask import Blueprint, request, jsonify
from app.models.user import User
from app.repositories.user_repo import UserRepository

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    try:
        user = User.from_dict(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    UserRepository.create(user)
    return jsonify({"status": "ok"}), 201

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = UserRepository.get_by_id(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(force=True)
    data['user_id'] = user_id
    try:
        user = User.from_dict(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    UserRepository.update(user)
    return jsonify({"status": "ok"}), 200