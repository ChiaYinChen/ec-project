"""Router for user."""
from typing import Any

from fastapi import APIRouter

from .. import exceptions as exc
from ..crud.user import CRUDUser
from ..schemas.user import User, UserCreate

router = APIRouter()


@router.post("", response_model=User, status_code=201)
async def create_user(user_in: UserCreate) -> Any:
    """
    ## Add new user

    required
    - **email**: user email (unique)
    - **password**: user password
    - **name**: each user must have a name

    optional
    - **is_active**: default to true
    - **is_superuser**: default to false
    """
    user = await CRUDUser.get_by_email(email=user_in.email)
    if user:
        raise exc.ConflictError("Email already registered")
    return await CRUDUser.create(obj_in=user_in)
