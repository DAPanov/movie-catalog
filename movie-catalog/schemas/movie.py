import random

from pydantic import BaseModel


class MovieBase(BaseModel):
    id: int = random.randint(4, 1000)
    title: str
    description: str
    year: int


class Movie(MovieBase):
    pass
