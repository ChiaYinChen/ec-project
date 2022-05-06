"""Exceptions handler."""
from typing import Any

import jose
from fastapi import Request
from fastapi.responses import JSONResponse

from app.main import app


class CustomError(Exception):
    """Custom error."""

    def __init__(self, status_code: int, message: Any):
        """Initialize."""
        self.status_code = status_code
        self.message = message


class UnauthenticatedError(CustomError):
    """Handle unauthenticated request."""

    def __init__(self, message):
        """Initialize."""
        self.status_code = 401
        self.message = message


class UnauthorizedError(CustomError):
    """Handle unauthorized request."""

    def __init__(self, message):
        """Initialize."""
        self.status_code = 403
        self.message = message


class ConflictError(CustomError):
    """Resource conflict error."""

    def __init__(self, message):
        """Initialize."""
        self.status_code = 409
        self.message = message


class NotFoundError(CustomError):
    """Resource not found error."""

    def __init__(self, message):
        """Initialize."""
        self.status_code = 404
        self.message = message


@app.exception_handler(CustomError)
async def custom_error_handler(request: Request, exc: CustomError):
    """Handle custom error."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(jose.exceptions.JWTError)
async def jose_exception_handler(
    request: Request, exc: jose.exceptions.JWTError
):
    """Handle jose exceptions."""
    if isinstance(exc, jose.exceptions.ExpiredSignatureError):
        return JSONResponse(
            status_code=401,
            content={"message": "Token expired"},
        )
    return JSONResponse(
        status_code=401,
        content={"message": "Could not validate credentials"},
    )
