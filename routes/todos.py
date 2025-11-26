import httpx
from fastapi import APIRouter

from utils.errors import handle_external_api_error

router = APIRouter()


@router.get("/")
async def get_todos():
    """Fetch todos from https://dummyjson.com/todos"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://dummyjson.com/todos")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise handle_external_api_error(e)


