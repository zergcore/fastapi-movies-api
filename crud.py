from sqlmodel import select

from config.database import SessionLocal
from models.movie import Movie
from models.user import User


def get_user(db: SessionLocal, user_id: int):
    statement = select(User).where(User.id == user_id)
    return db.exec(statement).first()


def get_user_by_email(db: SessionLocal, email: str):
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()


def get_users(db: SessionLocal, skip: int = 0, limit: int = 100):
    statement = select(User).offset(skip).limit(limit)
    return db.exec(statement).all()


def create_user_db(db: SessionLocal, user: User):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, password=fake_hashed_password, is_active=True)
    db.add(db_user)
    db.commit()
    return db_user


def get_movies(db: SessionLocal, skip: int = 0, limit: int = 100):
    statement = select(Movie).offset(skip).limit(limit)
    return db.exec(statement).all()


def create_movie(db: SessionLocal, movie: Movie):
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    return db_movie
