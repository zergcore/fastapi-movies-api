from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import uvicorn
import os

from schemas.user import UserCreate, User as UserModel
from database.movie import Movie
from config.database import Base, engine, SessionLocal
from utils.jwt_manager import create_token
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Movies API"
app.version = "0.0.1"
app.description = "API to get movies"
app.contact = {"name": "Zaidibeth Ramos", "email": "zergcoredev@gmail.com"}
app.license_info = {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
app.openapi_tags = [{"name": "Home", "description": "Home page"}]
app.debug = True

app.add_middleware(ErrorHandler)

app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

with open("movies.json") as f:
    movies = json.load(f)
    # db = SessionLocal()
    # for movie in movies:
    #     db_movie = Movie(**movie)
    #     db.add(db_movie)
    #     db.commit()
    #     db.refresh(db_movie)

#path operations
@app.get("/", tags=["Home"], response_class=JSONResponse, status_code=200, response_model=dict)
def message():
    return JSONResponse(content={"message": "Hello World"}, status_code=200)

@app.post('/login', tags=['Auth'])
def login(user: UserCreate):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 8000)))
