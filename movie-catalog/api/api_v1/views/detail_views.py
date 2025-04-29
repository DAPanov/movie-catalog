from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status

from api.api_v1.crud import storage
from api.api_v1.dependencies import prefetch_movie
from schemas.movie import (
    Movie,
    MovieUpdate,
    MoviePartialUpdate,
    MovieRead,
)

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


MovieBySlug = Annotated[Movie, Depends(prefetch_movie)]


@router.get("/", response_model=MovieRead)
def get_movie_by_id(movie: MovieBySlug) -> Movie:
    return movie


@router.put("/", response_model=MovieRead)
def update_movie(movie: MovieBySlug, movie_in: MovieUpdate) -> Movie:
    return storage.update(movie, movie_in)


@router.patch("/", response_model=MovieRead)
def update_movie_partial(movie: MovieBySlug, movie_in: MoviePartialUpdate) -> Movie:
    return storage.partial_update(movie, movie_in)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(movie: MovieBySlug) -> None:
    storage.delete(movie=movie)
