from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def read_root(
    request: Request,
) -> dict[str, str]:
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "Hello World",
        "docs": str(docs_url),
    }
