"""CRUD for user."""
from typing import Any

from ..core.security import get_password_hash, verify_password
from ..models.user import User as UserModel
from ..schemas.user import UserCreate


class CRUDUser:

    @classmethod
    async def get_by_email(
        cls, *, email: str
    ) -> UserModel | None:
        """Get user by email."""
        return await UserModel.objects.filter(email=email).get_or_none()

    @classmethod
    async def create(
        cls, *, obj_in: UserCreate | dict[str, Any]
    ) -> UserModel:
        """Create a user."""
        if isinstance(obj_in, dict):
            create_data = obj_in.copy()
        else:
            create_data = obj_in.dict()
        hashed_password = get_password_hash(create_data["password"])
        del create_data["password"]
        db_obj = UserModel(**create_data, hashed_password=hashed_password)
        return await db_obj.save()

    @staticmethod
    async def authenticate(
        *,
        email: str,
        password: str
    ) -> UserModel | None:
        """Authenticate a user."""
        user = await CRUDUser.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def is_active(user: UserModel) -> bool:
        """Check if user is active."""
        return user.is_active

    @staticmethod
    def is_superuser(user: UserModel) -> bool:
        """Check if user is superuser."""
        return user.is_superuser
