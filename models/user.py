from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    # password:str
    is_active: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                 "email": "user@email.com",
                 "password": "password",
                #  "is_active": False
                }
            ]
        },
        "from_attributes": True # orm_mode
    }

    # Notice that the User, the Pydantic model that will be used when reading a user (returning it from the API) doesn't include the password