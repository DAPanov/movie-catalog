from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    description: str = ""
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

    description: str
    year: int


class MovieCreate(Movie):
    """
    Модель для создания фильма
    """
