"""Schema for User."""
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base User schema."""
    email: EmailStr
    name: str = Field(..., max_length=32)
    is_active: bool | None = True
    is_superuser: bool | None = False


class UserCreate(UserBase):
    """Create input."""
    password: str = Field(..., min_length=6)


class User(UserBase):
    """Output."""
    id: UUID

    class Config:
        orm_mode = True
