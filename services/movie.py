import database
from models.movie import Movie

class MovieService:
  def __init__(self, db):
    self.db = db


  def get_movies(self, skip: int = 0, limit: int = 100):
    return self.db.query(database.movie.Movie).offset(skip).limit(limit).all()


  def get_movie(self, movie_id: int):
    return self.db.query(database.movie.Movie).filter(database.movie.Movie.id == movie_id).first()


  def get_movie_by_category(self, category: str):
    return self.db.query(database.movie.Movie).filter(database.movie.Movie.category.like("%" + category.lower() + "%")).all()


  def create_movie(self, movie: Movie):
    db_movie = database.movie.Movie(**movie.dict())
    self.db.add(db_movie)
    self.db.commit()
    self.db.refresh(db_movie)
    return db_movie


  def update_movie(self, movie_id: int, movie: Movie):
    result = self.get_movie(movie_id)
    result.title = movie.title
    result.budget = movie.budget
    result.revenue = movie.revenue
    result.rating = movie.rating
    result.votes = movie.votes
    result.duration = movie.duration
    result.category = movie.category
    result.director = movie.director
    result.genre = movie.genre
    result.year = movie.year
    self.db.commit()
    self.db.refresh(result)
    return result


  def delete_movie(self, movie_id: int):
      result = self.get_movie(movie_id)
      self.db.delete(result)
      self.db.commit()
      return result