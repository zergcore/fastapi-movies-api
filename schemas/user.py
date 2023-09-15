from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr = Field()


class UserCreate(UserBase):
    password: str = Field()


class User(UserBase):
    id: Optional[int] = None
    is_active: bool

    # Notice that the User, the Pydantic model that will be used when reading a user (returning it from the API) doesn't include the password