# from sqlalchemy.orm import Session
from config.database import SessionLocal

from database.movie import Movie
from database.user import User
from models.movie import Movie as MovieModel
from models.user import User as UserModel, UserCreate


def get_user(db: SessionLocal, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: SessionLocal, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: SessionLocal, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: SessionLocal, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_movies(db: SessionLocal, skip: int = 0, limit: int = 100):
    return db.query(Movie).offset(skip).limit(limit).all()


def create_movie(db: SessionLocal, movie: Movie):
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
