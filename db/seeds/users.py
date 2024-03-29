from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from db.models.user import User
from db.db_setup import environment, SCHEMA
from api.utils.users import create_user

def seed_users(db: Session):
    users = [
        User(email='demo@radai.com', password='password', is_active=True),
        # Add more users as necessary
    ]

    for user in users:
        create_user(db=db, user=user)
    
    db.flush()  # Flush the changes without committing to make them available in the same session

def undo_users(db: Session):
    if environment == "production":
        db.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.execute(text("DELETE FROM users"))

def undo_profiles(db: Session):
    if environment == "production":
        db.execute(f"TRUNCATE table {SCHEMA}.profiles RESTART IDENTITY CASCADE;")
    else:
        db.execute(text("DELETE FROM profiles"))
