from fastapi import FastAPI, Body
from models.movie import Movie

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
      "rating": 9.3,
      "votes": 678790,
      "budget": 16000000,
      "revenue": 136906000,
      "category": "Drama",
    },
    {
        "id": 2,
        "title": "The Godfather",
        "year": 1972,
        "director": "Francis Ford Coppola",
        "duration": "3h 17min",
        "genre": "Crime, Drama",
        "rating": 9.2,
        "votes": 4717185,
        "budget": 20000000,
        "revenue": 134000000,
        "category": "Drama",
    },
    {
        "id": 3,
        "title": "The Godfather: Part II",
        "year": 1974,
        "director": "Francis Ford Coppola",
        "duration": "3h 22min",
        "genre": "Crime, Drama",
        "rating": 9,
        "votes": 3194518,
        "budget": 20000000,
        "revenue": 107200000,
        "category": "Drama",
    },
    {
        "id": 4,
        "title": "The Dark Knight",
        "year": 2008,
        "director": "Christopher Nolan",
        "duration": "2h 32min",
        "genre": "Action, Crime, Drama",
        "rating": 9,
        "votes": 5933283,
        "budget": 20000000,
        "revenue": 152780000,
        "category": "Drama",
    },
    {
        "id": 5,
        "title": "12 Angry Men",
        "year": 1957,
        "director": "Sidney Lumet",
        "duration": "1h 36min",
        "genre": "Crime, Drama",
        "rating": 8.9,
        "votes": 364583,
        "budget": 5000000,
        "revenue": 4206166,
        "category": "Drama",
    },
]


@app.get("/", tags=["Home"])
def message():
    return {"message": "Hello World"}


@app.get("/movies", tags=["Movies"])
def index():
    return movies

@app.get("/movies/{id}", tags=["Movies"])
def index(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    else:
      return []

@app.get("/movies/", tags=["Movies"])
def index(category: str):
  return [movie for movie in movies if movie["category"].lower() == category.lower()]

@app.post("/movies", tags=["Movies"], response_model=list[Movie])
def index(movie: Movie):
    movies.append(movie)
    return movies

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

@app.patch("/movies/{id}", tags=["Movies"])
def index(id: int, movie: dict = Body(...)):
    for item in movies:
        if item["id"] == id:
            item.update(movie)
            return item
    else:
        return []

@app.delete("/movies/{id}", tags=["Movies"])
def index(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies
    else:
        return []
