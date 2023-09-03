from fastapi import FastAPI

app = FastAPI()
app.title = "Movies API"
app.version = "0.0.1"
app.description = "API to get movies"
# app.terms_of_service = "None yet"
app.contact = {
    "name": "Zaidibeth Ramos",
    "email": "zergcoredev@gmail.com"
    }
app.license_info = {
    "name": "MIT",
    "url": "https://opensource.org/licenses/MIT"
    }
app.openapi_tags = [
  {
    "name": "Home",
    "description": "Home page"
  }
]
app.debug = True

@app.get("/", tags=["Home"])
def message():
  return {"message": "Hello World"}

# @app.get("/movies", tags=["Movies"])
# def index(request):
#     return {"message": "Hello World"}

# @app.get("/movies/{id}", tags=["Movies"])
# def index(request, id):
#     return {"message": "Hello World"}

# @app.get("/movies/search", tags=["Movies"])
# def index(request, title):
#   return {"message": "Hello World"}
