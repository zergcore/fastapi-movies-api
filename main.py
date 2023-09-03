from fastapi import FastAPI

app = FastAPI()
app.title = "Movies API"
app.version = "0.0.1"
app.description = "API to get movies"
# app.terms_of_service = "None yet"
app.contact = {"name": "Zaidibeth Ramos", "email": "zergcoredev@gmail.com"}
app.license_info = {"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
app.openapi_tags = [{"name": "Home", "description": "Home page"}]
app.debug = True

movies = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        "year": 1994,
        "director": "Frank Darabont",
        "duration": "2h 22min",
        "genre": "Crime, Drama",
    },
    {
        "id": 2,
        "title": "The Godfather",
        "year": 1972,
        "director": "Francis Ford Coppola",
        "duration": "3h 17min",
        "genre": "Crime, Drama",
    },
    {
        "id": 3,
        "title": "The Godfather: Part II",
        "year": 1974,
        "director": "Francis Ford Coppola",
        "duration": "3h 22min",
        "genre": "Crime, Drama",
    },
    {
        "id": 4,
        "title": "The Dark Knight",
        "year": 2008,
        "director": "Christopher Nolan",
        "duration": "2h 32min",
        "genre": "Action, Crime, Drama",
    },
    {
        "id": 5,
        "title": "12 Angry Men",
        "year": 1957,
        "director": "Sidney Lumet",
        "duration": "1h 36min",
        "genre": "Crime, Drama",
    },
]


@app.get("/", tags=["Home"])
def message():
    return {"message": "Hello World"}


@app.get("/movies", tags=["Movies"])
def index():
    return movies

# @app.get("/movies/{id}", tags=["Movies"])
# def index(request, id):
#     return {"message": "Hello World"}

# @app.get("/movies/search", tags=["Movies"])
# def index(request, title):
#   return {"message": "Hello World"}
