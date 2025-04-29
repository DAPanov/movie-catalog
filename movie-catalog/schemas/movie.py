from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, Field


DescriptionString = Annotated[
    str,
    MaxLen(255),
]


class MovieBase(BaseModel):
    description: DescriptionString = ""
    year: int = ""


class Movie(MovieBase):
    """
    Модель для фильма
    """

    title: str
    slug: str


class MovieUpdate(MovieBase):
    """
    Модель для обновления фильма
    """

    description: DescriptionString
    year: int


class MoviePartialUpdate(MovieBase):
    """
    Модель для частичного обновления фильма
    """

    description: DescriptionString | None = None
    year: int | None = None


class MovieCreate(Movie):
    """
    Модель для создания фильма
    """
