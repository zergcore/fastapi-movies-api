from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import JSONResponse
from typing import List
from models.movie import Movie
from models.user import User
import json
from jwt_manager import create_token

app = FastAPI()
app.title = "Movies API"
app.version = "0.0.1"
app.description = "API to get movies"
# app.terms_of_service = "None yet"
app.contact = {"name": "Zaidibeth Ramos", "email": "zergcoredev@gmail.com"}
app.license_info = {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
app.openapi_tags = [{"name": "Home", "description": "Home page"}]
app.debug = True

with open("movies.json") as f:
    movies = json.load(f)


@app.get("/", tags=["Home"], response_class=JSONResponse, status_code=200, response_model=dict)
def message():
    return JSONResponse(content={"message": "Hello World"}, status_code=200)

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get("/movies", tags=["Movies"], response_model=List[Movie], status_code=200)
def index():
    return JSONResponse(content=movies, status_code=200)


@app.get("/movies/{id}", tags=["Movies"], response_model=Movie, status_code=200)
def index(id: int = Path(gt=0, le=len(movies))):
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item, status_code=200)
    else:
        return JSONResponse(content=[], status_code=404)


@app.get("/movies/", tags=["Movies"], response_model=List[Movie], status_code=200)
def index(category: str = Query(min_length=3, max_length=20)):
    data = [movie for movie in movies if movie["category"].lower() == category.lower()]
    if len(data) == 0:
        return JSONResponse(content=[], status_code=404)
    return JSONResponse(content=data, status_code=200)


@app.post("/movies", tags=["Movies"], response_model=dict, status_code=201)
def index(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={message: "Movie added successfully"}, status_code=201)


# @app.post("/movies", tags=["Movies"], response_model=list[Movie])
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
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["year"] = movie.year
            item["director"] = movie.director
            item["duration"] = movie.duration
            item["genre"] = movie.genre
            item["votes"] = movie.votes
            item["budget"] = movie.budget
            item["revenue"] = movie.revenue
            item["rating"] = movie.rating
            item["category"] = movie.category
            JSONResponse(content = {message: "Movie updated successfully"}, status_code = 200)
    else:
        return JSONResponse(content = {message: "Movie not found"}, status_code = 404)


@app.delete("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content = {message: "Movie deleted successfully"}, status_code = 200)
    else:
        return JSONResponse(content = {message: "Movie not found"}, status_code = 404)
