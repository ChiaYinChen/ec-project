"""Schema for Product."""
from uuid import UUID

from pydantic import BaseModel, Field

from ..schemas.utils import as_form


class ProductBase(BaseModel):
    """Base Product schema."""
    description: str | None = None
    discount_rate: float = Field(..., ge=0, le=1)


@as_form
class ProductCreate(ProductBase):
    """Create input."""
    title: str = Field(..., max_length=128)


class ProductUpdate(ProductBase):
    """Update input."""
    pass


class Product(ProductCreate):
    """Output."""
    id: UUID
    image: str | None

    class Config:
        orm_mode = True
