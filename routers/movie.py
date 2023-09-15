from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List

from models.movie import Movie as MovieModel
from database.movie import Movie
from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from crud import get_movies, create_movie_db, get_movie_by_id, get_movie_by_category, update_movie_db, delete_movie_db

movie_router = APIRouter()

@movie_router.get("/movies", tags=["Movies"], response_model=List[MovieModel], status_code=200, dependencies=[Depends(JWTBearer())])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = get_movies(db, skip=skip, limit=limit)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.get("/movies/{id}", tags=["Movies"], response_model=MovieModel, status_code=200)
def read_movie_by_id(id: int = Path(gt=0), db: Session = Depends(get_db)):
    result = get_movie_by_id(db, movie_id=id)
    if result:
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)


@movie_router.get("/movies/", tags=["Movies"], response_model=List[MovieModel], status_code=200)
def read_movie_by_category(category: str = Query(min_length=3, max_length=20),  db: Session = Depends(get_db)):
    result = get_movie_by_category(db, category=category)
    if result:
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        return JSONResponse(content={"message": "Category not found"}, status_code=404)


@movie_router.post("/movies", tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: MovieModel, db: Session = Depends(get_db)):
    create_movie_db(db=db, movie=movie)
    return JSONResponse(content={"message": "Movie added successfully"}, status_code=201)


@movie_router.put("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: MovieModel, db: Session = Depends(get_db)):
    result = get_movie_by_id(db, movie_id=id)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    else:
        update_movie_db(db, movie_id=id, movie=movie)
        return JSONResponse(content={"message": "Movie updated successfully"}, status_code=201)


@movie_router.delete("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int, db: Session = Depends(get_db)):
    result = get_movie_by_id(db, movie_id=id)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    else:
        delete_movie_db(db, movie_id=id)
        return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)

