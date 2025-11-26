from fastapi import FastAPI

from routes.items import router as items_router
from routes.todos import router as todos_router

app = FastAPI(title="Sample FastAPI app")

# Include routers
app.include_router(items_router, prefix="", tags=["items"])
app.include_router(todos_router, prefix="/todos", tags=["todos"])
