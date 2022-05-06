"""Router for auth."""
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .. import exceptions as exc
from ..core.security import create_access_token
from ..crud.user import CRUDUser
from ..schemas.token import Token

router = APIRouter()


@router.post("/access-token", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Create an access token for user which
    will get expire after 20 minutes.
    """
    user = await CRUDUser.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise exc.UnauthenticatedError("Incorrect username or password")
    elif not CRUDUser.is_active(user):
        raise exc.UnauthorizedError("Inactive user")
    return {
        "access_token": create_access_token(sub=user.email),
        "token_type": "bearer",
    }
