import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=2, max_length=50)
    year: int = Field(le=datetime.date.today().year)
    director: str = Field(min_length=8, max_length=25)
    duration: str = Field(min_length=5, max_length=10)
    genre: str = Field(min_length=3, max_length=15)
    rating: float = Field(gt=0, le=10)
    votes: int = Field(gt=0)
    budget: int = Field(gt=0)
    revenue: int = Field(gt=0)
    category: str = Field(min_length=3, max_length=15)
