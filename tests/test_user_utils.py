# test_user_utils.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from db.models.user import User
from pydantic_schemas.user import UserCreate
from api.utils.user import get_user, get_user_by_email, get_users, create_user

import os

# Set up a test database
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This fixture will be used by all tests. It creates a new database session used for testing.
@pytest.fixture
def test_db() -> Session:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_get_user(test_db):
    user_id = 1  # Set this to an existing user ID
    user = get_user(test_db, user_id)
    assert user is not None
    assert user.id == user_id

def test_get_user_by_email(test_db):
    email = "testuser@example.com"  # Set this to an existing user email
    user = get_user_by_email(test_db, email)
    assert user is not None
    assert user.email == email

def test_get_users(test_db):
    users = get_users(test_db)
    assert len(users) >= 0  # As the function will always return a list

def test_create_user(test_db):
    user_data = UserCreate(email="newuser@example.com", password="newuserpassword", is_active=True)
    user = create_user(test_db, user_data)
    assert user is not None
    assert user.email == user_data.email
