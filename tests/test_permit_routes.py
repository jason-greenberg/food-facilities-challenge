import pytest
from fastapi.testclient import TestClient
from main import app
from pydantic_schemas.permit import PermitCreate
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def auth_headers():
    # simulate login
    login_response = client.post("/token", data={"username": "demo@radai.com", "password": "password"})
    
    # get access token
    access_token = login_response.json().get("access_token")
    
    # return headers with Bearer token
    return {"Authorization": f"Bearer {access_token}"}

def test_read_permits(auth_headers):
    response = client.get("/permits/?skip=0&limit=10", headers=auth_headers)  
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 10  # As we have limited to 10 permits in this test

def test_get_nearest_food_trucks(auth_headers):
    lat, lon = 37.76201920035647, -122.42730642251331
    response = client.get(f"/permits/?latitude={lat}&longitude={lon}&status=APPROVED", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Print length of response
    print("Length of response: ", len(response.json()))
    assert len(response.json()) == 5  # As we need to fetch 5 nearest food trucks
    for permit in response.json():
        assert permit['status'] == "APPROVED"


def test_search_by_street(auth_headers):
    street_name = "SAN"
    response = client.get(f"/permits/?address={street_name}", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for permit in response.json():
        assert street_name in permit['address']

def test_search_by_applicant(auth_headers):
    applicant_name = "The Geez Freeze"
    response = client.get(f"/permits/?applicant={applicant_name}", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for permit in response.json():
        assert permit['applicant'] == applicant_name


def test_create_new_permit(auth_headers):
    permit_data = {
        "location_id": 1571753,
        "applicant": "The Geez Freeze",
        "facility_type": "Truck",
        "cnn": 887000,
        "location_description": "18TH ST: DOLORES ST to CHURCH ST (3700 - 3799)",
        "address": "3750 18TH ST",
        "blocklot": "3579006",
        "block": "3579",
        "lot": "006",
        "permit": "21MFF-00015",
        "status": "APPROVED",
        "food_items": "Snow Cones: Soft Serve Ice Cream & Frozen Virgin Daiquiris",
        "x": 6004575.869,
        "y": 2105666.974,
        "latitude": 37.76201920035647,
        "longitude": -122.42730642251331,
        "schedule": "http://bsm.sfdpw.org/PermitsTracker/reports/report.aspx?title=schedule&report=rptSchedule&params=permit=21MFF-00015&ExportPDF=1&Filename=21MFF-00015_schedule.pdf",
        "dayshours": None,
        "noisent": None,
        "approved": "2022-01-28T00:00:00Z",  # Notice the format, FastAPI typically expects ISO 8601
        "received": "2021-03-15T00:00:00Z",  # Notice the format, FastAPI typically expects ISO 8601
        "priorpermit": 0,
        "expirationdate": "2022-11-15T00:00:00Z",  # Notice the format, FastAPI typically expects ISO 8601
        "location": "(37.76201920035647, -122.42730642251331)",
        "fire_prevention_districts": 8,
        "police_districts": 4,
        "supervisor_districts": 5,
        "zip_codes": 28862,
        "neighborhoods_old": 3
    }

    response = client.post("/permits", json=permit_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["applicant"] == permit_data["applicant"]
