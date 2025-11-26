from fastapi import FastAPI

from routes.items import router as items_router
from routes.todos import router as todos_router
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Sample FastAPI app")

# Include routers
app.include_router(items_router, prefix="", tags=["items"])
app.include_router(todos_router, prefix="/todos", tags=["todos"])

logger.info("FastAPI application initialized successfully")
