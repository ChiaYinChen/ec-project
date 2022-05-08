"""Database ORM models for product."""
from datetime import datetime
from uuid import uuid4

import ormar

from ..models.base import BaseMeta
from ..models.brand import Brand


class Product(ormar.Model):
    """Table for product."""

    class Meta(BaseMeta):
        tablename = "product"
        constraints = [ormar.UniqueColumns("brand", "title")]

    id: str = ormar.UUID(
        primary_key=True,
        default=uuid4,
        nullable=False,
        index=True,
        uuid_format="string"
    )
    title: str = ormar.String(max_length=128, nullable=False)
    description: str = ormar.Text(nullable=True)
    discount_rate: int = ormar.Float(minimum=0, maximum=1, nullable=False)
    image: str = ormar.LargeBinary(
        nullable=True,
        max_length=20000000,
        represent_as_base64_str=True
    )
    created_time: datetime = ormar.DateTime(default=datetime.now)
    brand: Brand = ormar.ForeignKey(
        Brand,
        related_name="products",
        onupdate="CASCADE",
        ondelete="CASCADE"
    )
