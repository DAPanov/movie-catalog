import logging

from fastapi import FastAPI, Request

from api import router
from app_lifespan import lifespan
from core import config

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)

app = FastAPI(
    title="Movie catalog",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
async def root(
    request: Request,
) -> dict[str, str]:
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "Hello World",
        "docs": str(docs_url),
    }
