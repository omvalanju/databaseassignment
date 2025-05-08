from datetime import datetime

class User:
    def __init__(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        password_hash: str,
        email: str,
        gender: str = None,
        height_cm: float = None,
        weight_kg: float = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        if not user_id:
            raise ValueError("user_id is required")
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.email = email
        self.gender = gender
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password_hash": self.password_hash,
            "email": self.email,
            "gender": self.gender,
            "height_cm": self.height_cm,
            "weight_kg": self.weight_kg,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            user_id=data.get("user_id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            password_hash=data.get("password_hash"),
            email=data.get("email"),
            gender=data.get("gender"),
            height_cm=data.get("height_cm"),
            weight_kg=data.get("weight_kg"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )