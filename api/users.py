from db.db_setup import get_db
from pydantic_schemas.user import UserCreate, User, UserOut

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.users import get_user_by_email, create_user
from api.auth.token import get_current_active_user

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered.")
    return create_user(db=db, user=user)

@router.get("/current", response_model=UserOut)
async def read_current_user(
    current_user: User = Depends(get_current_active_user)
):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return current_user
