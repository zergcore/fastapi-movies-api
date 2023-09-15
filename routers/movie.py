from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List

from schemas.movie import Movie as MovieModel
from database.movie import Movie
from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()

@movie_router.get("/movies", tags=["Movies"], response_model=List[MovieModel], status_code=200, dependencies=[Depends(JWTBearer())])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = MovieService(db).get_movies(skip=skip, limit=limit)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.get("/movies/{id}", tags=["Movies"], response_model=MovieModel, status_code=200)
def read_movie_by_id(id: int = Path(gt=0), db: Session = Depends(get_db)):
    result = MovieService(db).get_movie(movie_id=id)
    if result:
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)


@movie_router.get("/movies/", tags=["Movies"], response_model=List[MovieModel], status_code=200)
def read_movie_by_category(category: str = Query(min_length=3, max_length=20),  db: Session = Depends(get_db)):
    result = MovieService(db).get_movie_by_category(category=category)
    if result:
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        return JSONResponse(content={"message": "Category not found"}, status_code=404)


@movie_router.post("/movies", tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: MovieModel, db: Session = Depends(get_db)):
    MovieService(db).create_movie(movie=movie)
    return JSONResponse(content={"message": "Movie added successfully"}, status_code=201)


@movie_router.put("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: MovieModel, db: Session = Depends(get_db)):
    result = MovieService(db).get_movie(movie_id=id)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    else:
        MovieService(db).update_movie(movie_id=id, movie=movie)
        return JSONResponse(content={"message": "Movie updated successfully"}, status_code=201)


@movie_router.delete("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int, db: Session = Depends(get_db)):
    result = MovieService(db).get_movie(movie_id=id)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    else:
        MovieService(db).delete_movie(movie_id=id)
        return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)

