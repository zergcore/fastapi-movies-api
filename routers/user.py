from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from models.user import UserCreate, User as UserModel
from database.user import User
from crud import get_user, get_user_by_email, get_users, create_user_db, update_user_db, delete_user_db
from config.database import SessionLocal, get_db

user_router = APIRouter()

@user_router.get("/users/", tags=["Users"], response_model=List[UserModel])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return JSONResponse(content=jsonable_encoder(users), status_code=200)


@user_router.get("/users/{user_id}", tags=["Users"], response_model=UserModel)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return JSONResponse(content=jsonable_encoder(db_user), status_code=200)


@user_router.post("/users/", tags=["Users"], response_model=UserModel)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        create_user_db(db=db, user=user)
        return JSONResponse(content={"message": "User added successfully"}, status_code=201)


@user_router.put("/users/{user_id}", tags=["Users"], response_model=UserModel)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        update_user_db(db=db, user_id=user_id, user=user)
        return JSONResponse(content={"message": "User updated successfully"}, status_code=201)


@user_router.delete("/users/{user_id}", tags=["Users"], response_model=UserModel)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = get_user(db, user_id=user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        delete_user_db(db=db, user_id=user_id)
        return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)