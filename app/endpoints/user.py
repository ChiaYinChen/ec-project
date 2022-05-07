"""Router for user."""
from typing import Any

from fastapi import APIRouter, Depends

from .. import exceptions as exc
from ..crud.user import CRUDUser
from ..deps import get_current_superuser_optional
from ..models.user import User as UserModel
from ..schemas.user import User, UserCreate

router = APIRouter()


@router.post(
    "",
    response_model=User,
    status_code=201,
    summary="Create User (login optional)",
)
async def create_user(
    user_in: UserCreate,
    current_user: UserModel | None = Depends(get_current_superuser_optional)
) -> Any:
    """
    ## Add new user

    required
    - **email**: user email (unique)
    - **password**: user password
    - **name**: each user must have a name

    optional
    - **is_active**: default to true
    - **is_superuser**: default to false

    notes
    - `is_active` and `is_superuser` only can be used by `admin`
    """
    user = await CRUDUser.get_by_email(email=user_in.email)
    if user:
        raise exc.ConflictError("Email already registered")
    if not current_user:
        user_in = user_in.dict(exclude={"is_active", "is_superuser"})
    return await CRUDUser.create(obj_in=user_in)
