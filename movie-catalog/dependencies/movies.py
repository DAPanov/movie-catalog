from typing import Annotated

from fastapi import Depends, Request

from storage.movies import MovieStorage


def get_movies_storage(request: Request) -> MovieStorage:
    return request.app.state.movies_storage


GetMoviesStorage = Annotated[
    MovieStorage,
    Depends(get_movies_storage),
]
