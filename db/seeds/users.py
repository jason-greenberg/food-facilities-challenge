from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from db.models.user import User
from db.db_setup import environment, SCHEMA

def seed_users(db: Session):
    students = [
        User(email='student1@aa.io', password='student', is_active=True),
        User(email='student2@aa.io', password='student', is_active=True),
        User(email='student3@aa.io', password='student', is_active=True),
    ]

    for user in students:
        db.add(user)
    
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
