from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    slug: str
    title: str
    description: str
    year: int


class MovieCreate(MovieBase):
    """
    Модель для создания фильма
    """


class Movie(MovieBase):
    """
    Модель для фильма
    """
