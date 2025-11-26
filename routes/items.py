from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


@router.get("/")
async def root():
    logger.info("GET / - App status check")
    return {"message": "FastAPI is running"}


@router.get("/hello")
async def hello():
    logger.info("GET /hello - Hello endpoint called")
    return {"message": "Hello, world!"}


@router.post("/items/")
async def create_item(item: Item):
    logger.info(f"POST /items/ - Creating item: {item.name} (${item.price})")
    return {"item": item, "message": "Item created"}
