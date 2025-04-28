from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    id: int
    title: str
    description: str
    year: int


class MovieCreate(BaseModel):
    """
    Модель для создания фильма
    """

    title: str
    description: str
    year: int


class Movie(MovieBase):
    """
    Модель для фильма
    """
