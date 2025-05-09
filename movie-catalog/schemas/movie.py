from typing import Annotated

from annotated_types import MaxLen, Len
from pydantic import BaseModel, Field


DescriptionString = Annotated[
    str,
    MaxLen(255),
]


class MovieBase(BaseModel):
    title: str
    description: DescriptionString = ""
    year: int


class Movie(MovieBase):
    """
    Модель для фильма
    """

    slug: Annotated[str, Len(min_length=1, max_length=25)]
    notes: str = "Admins notes"


class MovieRead(MovieBase):
    """
    Схема для чтения данных о фильме
    """

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

    title: str | None = None
    description: DescriptionString | None = None
    year: int | None = None


class MovieCreate(MovieBase):
    """
    Модель для создания фильма
    """

    slug: Annotated[str, Len(min_length=1, max_length=25)]
