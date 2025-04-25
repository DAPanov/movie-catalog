from typing import Annotated

from fastapi import APIRouter, Depends
from api.api_v1.crud import MOVIE_LIST
from api.api_v1.dependecies import prefetch_movie
from schemas.movie import Movie

router = APIRouter(tags=["Movies"])


@router.get("/movie-list", response_model=list[Movie])
async def get_movies_list() -> list[Movie]:
    return MOVIE_LIST


@router.get("/movie/{movie_id}", response_model=Movie)
async def get_movie_by_id(movie: Annotated[Movie, Depends(prefetch_movie)]):
    return movie
