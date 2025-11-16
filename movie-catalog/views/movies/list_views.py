from typing import Any

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from dependencies.movies import GetMoviesStorage
from templating import templates

router = APIRouter()


@router.get(
    "/",
    name="movies:list",
    response_class=HTMLResponse,
)
def list_views(
    request: Request,
    storage: GetMoviesStorage,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    movies = storage.get()
    context.update(
        movies=movies,
    )
    return templates.TemplateResponse(
        request=request,
        name="movies/list.html",
        context=context,
    )
