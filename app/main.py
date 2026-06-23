from fastapi import FastAPI

from app.config import settings
from app.routers import items

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A simple inventory management REST API with in-memory storage.",
)

app.include_router(items.router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}
