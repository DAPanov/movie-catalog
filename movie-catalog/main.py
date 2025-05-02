import logging

from fastapi import FastAPI, Request
from api import router

from core import config

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)

app = FastAPI(
    title="Movie catalog",
)

app.include_router(router)


@app.get("/")
async def root(
    request: Request,
):
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "Hello World",
        "docs": str(docs_url),
    }
