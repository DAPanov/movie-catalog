from pydantic import BaseModel


class MovieBase(BaseModel):
    id: int
    title: str
    description: str
    year: int


class Movie(MovieBase):
    pass
