"""Dependencies."""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from . import exceptions as exc
from .core.config import settings
from .core.security import decode_token
from .crud.user import CRUDUser
from .models.user import User as UserModel

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/access-token",
    auto_error=False
)


async def get_user_from_token(
    token: str | None = Depends(reusable_oauth2)
) -> UserModel | None:
    """Get user from token."""
    if token is None:
        return None
    token_data = decode_token(token=token)
    if token_data.type != "access_token":
        raise exc.UnauthenticatedError("Invalid token type")
    user = await CRUDUser.get_by_email(email=token_data.sub)
    if not user:
        raise exc.NotFoundError("User not found")
    return user


async def get_current_user(
    current_user: UserModel | None = Depends(get_user_from_token)
) -> UserModel:
    """Get current active user (required)."""
    if not current_user:
        raise exc.UnauthenticatedError("Not authenticated")
    return current_user


async def get_current_user_optional(
    current_user: UserModel | None = Depends(get_user_from_token)
) -> UserModel | None:
    """Get current active user (optional)."""
    return current_user


async def get_current_superuser_optional(
    current_user: UserModel | None = Depends(get_current_user_optional),
) -> UserModel | None:
    """Get current active superuser (optional)."""
    if not current_user:
        return current_user
    if not CRUDUser.is_superuser(current_user):
        raise exc.UnauthorizedError("The user doesn't have enough privileges")
    return current_user
