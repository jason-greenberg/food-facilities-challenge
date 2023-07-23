from sqlalchemy.orm import Session

from db.models.user import User
from pydantic_schemas.user import UserCreate

from api.auth.password_utils import get_password_hash

# get user by id
def get_user(db: Session, user_id: int):
    return db.query(User).get(user_id)

# get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# get users list
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# create user
def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, is_active=user.is_active)
    db_user.password = get_password_hash(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
