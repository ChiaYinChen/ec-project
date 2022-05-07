"""Main app."""
from fastapi import FastAPI

from .core.config import settings
from .db.session import database
from .endpoints import auth, brand, index, user

app = FastAPI()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


app.include_router(index.router)
app.include_router(user.router, prefix=f"{settings.API_PREFIX}/users", tags=["users"])  # noqa: E501
app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["auth"])  # noqa: E501
app.include_router(brand.router, prefix=f"{settings.API_PREFIX}/brands", tags=["brands"])  # noqa: E501
