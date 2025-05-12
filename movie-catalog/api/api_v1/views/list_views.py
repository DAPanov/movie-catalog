from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
)


from api.api_v1.crud import storage, MovieAlreadyExistsError
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
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Movie already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug='name' already exists.",
                    }
                }
            },
        },
    },
)
def create_movie(movie_create: MovieCreate) -> Movie:
    try:
        return storage.create_or_raise_if_exists(movie_create)
    except MovieAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie with slug={movie_create.slug!r} already exists",
        )
