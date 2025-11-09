from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def read_root(
    request: Request,
    name: str = "World",
) -> dict[str, str]:
    docs_url = request.url.replace(path="/docs")
    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }
