from sqlmodel import Field, SQLModel
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(min_length=8)
    password:str = Field(min_length=8)
    is_active: bool = Field(default=True)
