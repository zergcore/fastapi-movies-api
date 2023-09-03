from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str
    year: int
    director: str
    duration: str
    genre: str
    rating: float
    votes: int
    budget: int
    revenue: int
    category: str