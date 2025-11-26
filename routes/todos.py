import httpx
from fastapi import APIRouter

from utils.errors import handle_external_api_error
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/")
async def get_todos():
    """Fetch todos from https://dummyjson.com/todos"""
    logger.info("Fetching todos from external API")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://dummyjson.com/todos")
            response.raise_for_status()
            todos = response.json()
            logger.info(f"Successfully fetched {len(todos.get('todos', []))} todos")
            return todos
    except Exception as e:
        logger.error(f"Error fetching todos: {type(e).__name__}: {str(e)}", exc_info=True)
        raise handle_external_api_error(e)


