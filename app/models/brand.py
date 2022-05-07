"""Database ORM models for brand."""
from datetime import datetime
from uuid import uuid4

import ormar
from sqlalchemy.sql import expression

from ..models.base import BaseMeta
from ..models.user import User


class Brand(ormar.Model):
    """Table for brand."""

    class Meta(BaseMeta):
        tablename = "brand"
        constraints = [ormar.UniqueColumns("owner", "name")]

    id: str = ormar.UUID(
        primary_key=True,
        default=uuid4,
        nullable=False,
        index=True,
        uuid_format="string"
    )
    name: str = ormar.String(max_length=64, nullable=False)
    about: str = ormar.Text(nullable=True)
    social_media: str = ormar.String(max_length=256, nullable=True)
    website: str = ormar.String(max_length=256, nullable=True)
    email: str = ormar.String(max_length=128, nullable=True)
    phone: str = ormar.String(max_length=128, nullable=True)
    created_time: datetime = ormar.DateTime(default=datetime.now)
    is_active: bool = ormar.Boolean(
        server_default=expression.true(),
        default=True
    )
    owner: User = ormar.ForeignKey(
        User,
        related_name="brands",
        onupdate="CASCADE",
        ondelete="CASCADE"
    )
