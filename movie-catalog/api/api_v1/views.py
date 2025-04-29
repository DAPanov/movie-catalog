import random
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
    Form,
)
from api.api_v1.crud import storage
from api.api_v1.dependencies import prefetch_movie
from schemas.movie import Movie, MovieCreate

router = APIRouter(tags=["Movies"])


@router.get("/movie-list", response_model=list[Movie])
async def get_movies_list() -> list[Movie]:
    return storage.get()


@router.get("/movie/{slug}", response_model=Movie)
async def get_movie_by_id(movie: Annotated[Movie, Depends(prefetch_movie)]) -> Movie:
    return movie


@router.post("/movie", response_model=Movie, status_code=status.HTTP_201_CREATED)
async def create_movie(movie_create: MovieCreate) -> Movie:
    return storage.create(movie_create)


@router.delete(
    "/movie/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
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
async def delete_movie(movie: Annotated[Movie, Depends(prefetch_movie)]) -> None:
    storage.delete(movie=movie)
