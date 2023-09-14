from fastapi import FastAPI, Body, Path, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
import json

from models.movie import Movie as MovieModel
from models.user import User as UserModel, UserCreate
from crud import get_movies, get_user, get_user_by_email, get_users
from config.database import Base, SessionLocal, engine
from jwt_manager import create_token
from database.movie import Movie
from database.user import User
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer

app = FastAPI()
app.title = "Movies API"
app.version = "0.0.1"
app.description = "API to get movies"
app.contact = {"name": "Zaidibeth Ramos", "email": "zergcoredev@gmail.com"}
app.license_info = {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
app.openapi_tags = [{"name": "Home", "description": "Home page"}]

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

app.debug = True

with open("movies.json") as f:
    movies = json.load(f)

#path operations
@app.get("/", tags=["Home"], response_class=JSONResponse, status_code=200, response_model=dict)
def message():
    return JSONResponse(content={"message": "Hello World"}, status_code=200)

@app.post('/login', tags=['auth'])
def login(user: UserCreate):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.post("/users/", tags=["Users"], response_model=UserModel)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.get("/users/", tags=["Users"], response_model=list[UserModel])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", tags=["Users"], response_model=UserModel)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/movies", tags=["Movies"], response_model=List[MovieModel], status_code=200, dependencies=[Depends(JWTBearer())])
def index():
    db = SessionLocal()
    result = db.query(Movie).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@app.get("/movies/{id}", tags=["Movies"], response_model=MovieModel, status_code=200)
def index(id: int = Path(gt=0)):
    db = SessionLocal()
    result = db.query(Movie).filter(Movie.id == id).first()
    if result:
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    # for item in movies:
    #     if item["id"] == id:
    #         return JSONResponse(content=item, status_code=200)
    # else:
    #     return JSONResponse(content=[], status_code=404)


@app.get("/movies/", tags=["Movies"], response_model=List[MovieModel], status_code=200)
def index(category: str = Query(min_length=3, max_length=20)):
    db = SessionLocal()
    result = db.query(Movie).filter(Movie.category.like("%" + category.lower() + "%")).all()
    if result:
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        return JSONResponse(content={"message": "Category not found"}, status_code=404)
    # data = [movie for movie in movies if movie["category"].lower() == category.lower()]
    # if len(data) == 0:
    #     return JSONResponse(content=[], status_code=404)
    # return JSONResponse(content=data, status_code=200)


@app.post("/movies", tags=["Movies"], response_model=dict, status_code=201)
def index(movie: MovieModel):
    db = SessionLocal()
    new_movie = Movie(**movie.model_dump())
    # movies.append(movie)
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie added successfully"}, status_code=201)


# @app.post("/movies", tags=["Movies"], response_model=list[MovieModel])
# def index(id: int = Body(...), title: str = Body(...), year: int = Body(...), director: str = Body(...), duration: str = Body(...), genre: str = Body(...), rating: float = Body(...), votes: int = Body(...), budget: int = Body(...), revenue: int = Body(...), category: str = Body(...)):
# movie = {
#     "id": id,
#     "title": title,
#     "year": year,
#     "director": director,
#     "duration": duration,
#     "genre": genre,
#     "rating": rating,
#     "votes": votes,
#     "budget": budget,
#     "revenue": revenue,
#     "category": category,
# }

@app.put("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: MovieModel):
    db = SessionLocal()
    result = db.query(Movie).filter(Movie.id == id).first()
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    else:
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
        return JSONResponse(content={"message": "Movie updated successfully"}, status_code=201)
    
    # for item in movies:
    #     if item["id"] == id:
    #         item["title"] = movie.title
    #         item["year"] = movie.year
    #         item["director"] = movie.director
    #         item["duration"] = movie.duration
    #         item["genre"] = movie.genre
    #         item["votes"] = movie.votes
    #         item["budget"] = movie.budget
    #         item["revenue"] = movie.revenue
    #         item["rating"] = movie.rating
    #         item["category"] = movie.category
    #         JSONResponse(content = {message: "Movie updated successfully"}, status_code = 200)
    # else:
    #     return JSONResponse(content = {message: "Movie not found"}, status_code = 404)


@app.delete("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int):
    db = SessionLocal()
    result = db.query(Movie).filter(Movie.id == id).first()
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    else:
        db.delete(result)
        db.commit()
        return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)
    # for item in movies:
    #     if item["id"] == id:
    #         movies.remove(item)
    #         return JSONResponse(content = {message: "Movie deleted successfully"}, status_code = 200)
    # else:
    #     return JSONResponse(content = {message: "Movie not found"}, status_code = 404)
    

# @app.post("/movies/", response_model=MovieModel)
# def create_movie(
#     movie: MovieModel, db: Session = Depends(get_db)
# ):
#     return create_movie(db=db, movie=movie)


# @app.get("/movie/", response_model=list[MovieModel])
# def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     movies = get_movies(db, skip=skip, limit=limit)
#     return movies
