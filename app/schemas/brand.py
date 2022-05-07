"""Schema for Brand."""
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, root_validator

from .. import exceptions as exc


class BrandBase(BaseModel):
    """Base Brand schema."""
    about: str | None = None
    social_media: str = Field(None, max_length=256)
    website: str = Field(None, max_length=256)
    email: EmailStr | None = None
    phone: str = Field(None, max_length=128)


class BrandCreate(BrandBase):
    """Create input."""
    name: str = Field(..., max_length=64)

    @root_validator(pre=True)
    def check_contact(cls, values: dict[str, Any]):
        filtered = {k: v for k, v in values.items() if v is not None}
        if any(key in filtered for key in {"social_media", "website", "email", "phone"}):  # noqa: E501
            return values
        raise exc.FormatError("must contain at least one contact info")


class BrandUpdate(BrandBase):
    """Update input."""
    is_active: bool | None = True


class Brand(BrandCreate):
    """Output."""
    id: UUID

    class Config:
        orm_mode = True
