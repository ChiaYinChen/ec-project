"""Security."""
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from ..core.config import settings
from ..schemas.token import TokenPayload

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(sub: str) -> str:
    """Create access token."""
    return _encode_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _encode_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    """Encode token."""
    utc_now = datetime.utcnow()
    payload = {
        "type": token_type,
        "iat": utc_now,
        "exp": utc_now + lifetime,
        "sub": str(sub)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  # noqa: E501


def decode_token(token: str) -> TokenPayload:
    """Decode token."""
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    token_data = TokenPayload(**payload)
    return token_data


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Encode password."""
    return PWD_CONTEXT.hash(password)
