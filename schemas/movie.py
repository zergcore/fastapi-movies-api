from pydantic import BaseModel, Field
from typing import Optional
import datetime

class Movie(BaseModel):
    id: Optional[int] = None
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
