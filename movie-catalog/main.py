from fastapi import FastAPI, Request
from api import router

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
