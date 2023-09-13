from pydantic import BaseModel, Field
import datetime

class Movie(BaseModel):
    '''
    __tablename__ = 'movies'

    id = Column(Integer, primary_key = True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)
    '''

    id: int = Field(gt=0)
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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "year": 2022,
                    "director": "Mi Director",
                    "duration": "2h 22min",
                    "genre": "Acción",
                    "rating": 9.9,
                    "votes": 999999,
                    "budget": 999999,
                    "revenue": 999999,
                    "category": "Acción"
                }
            ]
        }
    }