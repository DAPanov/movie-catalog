from fastapi import (
    APIRouter,
    status,
    BackgroundTasks,
    Depends,
)


from api.api_v1.crud import storage
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

from api.api_v1.dependencies import save_storage_state, api_token_required

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        Depends(save_storage_state),
        Depends(api_token_required),
    ],
)


@router.get("/", response_model=list[MovieRead])
def get_movies_list() -> list[Movie]:
    return storage.get()


@router.post("/", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def create_movie(movie_create: MovieCreate) -> Movie:
    return storage.create(movie_create)
