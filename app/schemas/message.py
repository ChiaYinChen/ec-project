"""Schema for Message."""
from typing import Any

from pydantic import BaseModel


class Message(BaseModel):
    """Output."""
    message: Any
