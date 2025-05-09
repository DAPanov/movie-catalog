from fastapi import (
    APIRouter,
    status,
    Depends,
)


from api.api_v1.crud import storage
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

from api.api_v1.dependencies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    }
                }
            },
        },
    },
)


@router.get("/", response_model=list[MovieRead])
def get_movies_list() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create: MovieCreate) -> Movie:
    return storage.create(movie_create)
