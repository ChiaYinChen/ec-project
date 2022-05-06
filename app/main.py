"""Main app."""
from fastapi import FastAPI

from .core.config import settings
from .db.session import database, engine, metadata
from .endpoints import index, user

metadata.create_all(bind=engine)
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
