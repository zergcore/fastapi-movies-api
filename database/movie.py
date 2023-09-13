from config.database import Base
from sqlalchemy import Column, String, Integer, Float

class Movie(Base):
    __tablename__ = 'movies'

    # Columns
    id = Column(Integer, primary_key = True)
    title = Column(String)
    year = Column(Integer)
    director = Column(String)
    duration = Column(String)
    genre = Column(String)
    rating = Column(Float)
    votes = Column(Integer)
    budget = Column(Integer)
    revenue = Column(Integer)
    category = Column(String)
