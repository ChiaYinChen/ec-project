"""Exceptions handler."""
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

from app.main import app


class CustomError(Exception):
    """Custom error."""

    def __init__(self, status_code: int, message: Any):
        """Initialize."""
        self.status_code = status_code
        self.message = message


class ConflictError(CustomError):
    """Resource conflict error."""

    def __init__(self, message):
        """Initialize."""
        self.status_code = 409
        self.message = message


@app.exception_handler(CustomError)
async def custom_error_handler(request: Request, exc: CustomError):
    """Handle custom error."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
