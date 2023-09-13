from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    email: str = Field(primary_key=True)
    password:str
    is_active: bool

    # Notice that the User, the Pydantic model that will be used when reading a user (returning it from the API) doesn't include the password