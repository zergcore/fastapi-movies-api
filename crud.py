from sqlalchemy.orm import Session

import database
from models.movie import Movie
from models.user import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(database.user.User).filter(database.user.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(database.user.User).filter(database.user.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.user.User).offset(skip).limit(limit).all()


def create_user_db(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = database.user.User(email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

def update_user_db(db: Session, user_id: int, user: UserCreate):
    result = get_user(db, user_id=user_id)
    result.email = user.email
    result.password = user.password
    db.commit()
    db.refresh(result)
    return result

def delete_user_db(db: Session, user_id: int):
    result = get_user(db, user_id=user_id)
    db.delete(result)
    db.commit()
    return result

def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.movie.Movie).offset(skip).limit(limit).all()


def get_movie_by_id(db: Session, movie_id: int):
    return db.query(database.movie.Movie).filter(database.movie.Movie.id == movie_id).first()


def get_movie_by_category(db: Session, category: str):
    return db.query(database.movie.Movie).filter(database.movie.Movie.category.like("%" + category.lower() + "%")).all()


def create_movie_db(db: Session, movie: Movie):
    db_movie = database.movie.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie_db(db: Session, movie_id: int, movie: Movie):
    result = get_movie_by_id(db, movie_id)
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
    db.commit()
    db.refresh(result)
    return result


def delete_movie_db(db: Session, movie_id: int):
    result = get_movie_by_id(db, movie_id)
    db.delete(result)
    db.commit()
    return result

