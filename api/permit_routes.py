from db.db_setup import get_db
from pydantic_schemas.user import UserCreate, User, UserOut

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.users import get_user_by_email, create_user
from api.auth.token import get_current_active_user

router = APIRouter()
