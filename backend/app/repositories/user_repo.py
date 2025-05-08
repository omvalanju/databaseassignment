from app.database.mongodb import get_users_collection
from app.models.user import User
from datetime import datetime

class UserRepository:
    @staticmethod
    def create(user: User) -> None:
        users = get_users_collection()
        now = datetime.utcnow()
        user.created_at = now
        user.updated_at = now
        users.insert_one(user.to_dict())

    @staticmethod
    def update(user: User) -> None:
        user.updated_at = datetime.utcnow()
        users = get_users_collection()
        users.update_one(
            {"user_id": user.user_id},
            {"$set": user.to_dict()},
            upsert=True
        )

    @staticmethod
    def get_by_id(user_id: str) -> User:
        users = get_users_collection()
        data = users.find_one({"user_id": user_id})
        if not data:
            return None
        return User.from_dict(data)