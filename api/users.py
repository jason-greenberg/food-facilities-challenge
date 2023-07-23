from typing import List

from db.db_setup import get_db
from pydantic_schemas.user import UserCreate, User

from fastapi import APIRouter, Path, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.users import get_user, get_user_by_email, get_users, create_user

router = APIRouter()

@router.get("/users", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/users", response_model=User, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered.")
    return create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

# @router.get("/users/{user_id}/courses", response_model=List[Course])
# async def get_courses_by_user_id(user_id: int, db: Session = Depends(get_db)):
#     courses = get_user_courses(user_id=user_id, db=db)
#     return courses
