from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from templating import templates

router = APIRouter()


@router.get(
    "/",
    name="home",
)
async def home_page(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    features = [
        "Unlimited number of movies",
        "Rate your favorite movie",
        "Personal watchlist",
    ]

    context.update(
        features=features,
    )
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )


@router.get(
    "/about/",
    name="about",
)
def about_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
    )
