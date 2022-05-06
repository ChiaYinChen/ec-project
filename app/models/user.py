"""Database ORM models for user."""
from datetime import datetime
from uuid import uuid4

import ormar
from sqlalchemy.sql import expression

from ..models.base import BaseMeta


class User(ormar.Model):
    """Table for user."""

    class Meta(BaseMeta):
        tablename = "user"

    id: str = ormar.UUID(
        primary_key=True,
        default=uuid4,
        nullable=False,
        index=True
    )
    email: str = ormar.String(
        max_length=128,
        unique=True,
        nullable=False,
        index=True
    )
    hashed_password: str = ormar.String(
        max_length=256,
        nullable=False,
        name="password"
    )
    name: str = ormar.String(max_length=32, nullable=False)
    created_time: datetime = ormar.DateTime(default=datetime.now)
    is_active: bool = ormar.Boolean(
        server_default=expression.true(),
        default=True
    )
    is_superuser: bool = ormar.Boolean(
        server_default=expression.false(),
        default=False
    )
