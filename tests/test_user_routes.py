import pytest
from fastapi.testclient import TestClient
from main import app

from random import randint

client = TestClient(app)

@pytest.fixture
def auth_headers():
    # simulate login
    login_response = client.post("/token", data={"username": "demo@radai.com", "password": "password"})
    
    # get access token
    access_token = login_response.json().get("access_token")
    
    # return headers with Bearer token
    return {"Authorization": f"Bearer {access_token}"}

def test_create_new_user(auth_headers):
    user_data = {
        "email": f"test_user{randint(1,10000)}@demo.com",
        "password": "password"
    }

    response = client.post("/users", json=user_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]

def test_create_existing_user(auth_headers):
    user_data = {
        "email": "demo@radai.com",  # existing user email
        "password": "password"
    }

    response = client.post("/users", json=user_data, headers=auth_headers)
    assert response.status_code == 400  # should return 400 error

def test_get_current_user(auth_headers):
    response = client.get("/users/current", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "demo@radai.com"

def test_get_current_user_unauthenticated():
    response = client.get("/users/current")  # No headers provided
    assert response.status_code == 401  # should return 401 unauthorized
