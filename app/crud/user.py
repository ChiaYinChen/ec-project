"""CRUD for user."""
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
        cls, *, obj_in: UserCreate
    ) -> UserModel:
        """Create a user."""
        hashed_password = get_password_hash(obj_in.password)
        db_obj = UserModel(
            **obj_in.dict(exclude={"password"}),
            hashed_password=hashed_password
        )
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
