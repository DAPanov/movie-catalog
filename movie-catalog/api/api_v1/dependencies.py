import logging

from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    status,
    Request,
    Header,
    Depends,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)

from api.api_v1.crud import storage
from core import config
from core.config import (
    USERS_DB,
)
from schemas.movie import Movie
from .redis import redis_tokens

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)

static_api_token = HTTPBearer(
    scheme_name="Static API Token",
    description="Your Static API Token for developer portal",
    auto_error=False,
)


user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic username + password auth",
    auto_error=False,
)


def prefetch_movie(slug: str) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug)
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug={slug!r} not found",
    )


def save_storage_state(request: Request, background_tasks: BackgroundTasks):
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add save storage state to background tasks")
        background_tasks.add_task(storage.save_to_file)


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
):
    if redis_tokens.token_exists(
        api_token.credentials,
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    validate_api_token(api_token=api_token)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
):
    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        log.info(
            "Username = %s and password = %s",
            credentials.username,
            credentials.password,
        )
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    validate_basic_auth(
        credentials=credentials,
    )


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        return validate_basic_auth(credentials=credentials)
    if api_token:
        return validate_api_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API Token or basic auth required",
    )
