from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from starlette import status

from schemas.movie import Movie

app = FastAPI(
    title="Movie catalog",
)

MOVIE_LIST = [
    Movie(
        id=1,
        title="The Shawshank Redemption",
        description="A banker convicted of uxoricide forms a friendship over a quarter century with a hardened convict,\n"
        " while maintaining his innocence and trying to remain hopeful through simple compassion.",
        year=1994,
    ),
    Movie(
        id=2,
        title="The Godfather",
        description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        year=1972,
    ),
    Movie(
        id=3,
        title="The Dark Knight",
        description="When a menace known as the Joker wreaks havoc and chaos on the people of Gotham,\n"
        " Batman, James Gordon and Harvey Dent must work together to put an end to the madness.",
        year=2008,
    ),
]


@app.get("/")
async def root(
    request: Request,
):
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "Hello World",
        "docs": str(docs_url),
    }


@app.get("/movie-list", response_model=list[Movie])
async def get_movies_list() -> list[Movie]:
    return MOVIE_LIST


@app.get("/movie/{movie_id}", response_model=Movie)
async def get_movie_by_id(movie_id: int):
    movie: Movie | None = next(
        (movie for movie in MOVIE_LIST if movie.id == movie_id),
        None,
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with id={movie_id} not found",
    )
