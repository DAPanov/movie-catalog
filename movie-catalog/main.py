import logging

from fastapi import FastAPI

from api import router
from app_lifespan import lifespan
from core.config import settings
from views import router as views_router

logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
    datefmt=settings.logging.date_format,
)

app = FastAPI(
    title="Movie catalog",
    lifespan=lifespan,
)

app.include_router(router)
app.include_router(views_router)
