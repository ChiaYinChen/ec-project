"""Router for index."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def index():
    """Index."""
    return {"message": "Hello!"}
