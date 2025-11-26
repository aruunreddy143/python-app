from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


@router.get("/")
async def root():
    return {"message": "FastAPI is running"}


@router.get("/hello")
async def hello():
    return {"message": "Hello, world!"}


@router.post("/items/")
async def create_item(item: Item):
    return {"item": item, "message": "Item created"}
