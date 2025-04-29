from fastapi import (
    APIRouter,
    status,
)
from api.api_v1.crud import storage
from schemas.movie import Movie, MovieCreate

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=list[Movie])
async def get_movies_list() -> list[Movie]:
    return storage.get()


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
async def create_movie(movie_create: MovieCreate) -> Movie:
    return storage.create(movie_create)
