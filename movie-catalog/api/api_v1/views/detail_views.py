from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status

from api.api_v1.crud import storage
from api.api_v1.dependencies import prefetch_movie
from schemas.movie import Movie


router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with 'slug' not found",
                    },
                },
            },
        }
    },
)


@router.get("/", response_model=Movie)
async def get_movie_by_id(movie: Annotated[Movie, Depends(prefetch_movie)]) -> Movie:
    return movie


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_movie(movie: Annotated[Movie, Depends(prefetch_movie)]) -> None:
    storage.delete(movie=movie)
