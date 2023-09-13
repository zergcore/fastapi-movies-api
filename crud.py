from sqlalchemy.orm import Session

import database, models


def get_user(db: Session, user_id: int):
    return db.query(database.user.User).filter(database.user.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(database.user.User).filter(database.user.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.user.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: models.user.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = database.User(email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.movie.Movie).offset(skip).limit(limit).all()


def create_movie(db: Session, movie: models.movie.Movie):
    db_movie = database.movie.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie