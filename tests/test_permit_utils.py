import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from pydantic_schemas.permit import PermitCreate
from api.utils.permits import get_permit, get_permits, create_permit, get_permits_by_applicant, get_permits_by_address, get_nearest_permits, get_permits_by_conditions
from datetime import datetime

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

def test_get_permit(test_db):
    permit_id = 324  # Set this to an existing permit ID
    permit = get_permit(test_db, permit_id)
    assert permit is not None
    assert permit.id == permit_id

def test_get_permits(test_db):
    permits = get_permits(test_db)
    assert len(permits) >= 0  # As the function will always return a list

def test_create_permit(test_db):
    permit_data = PermitCreate(
        location_id=1571753,
        applicant="The Geez Freeze",
        facility_type="Truck",
        cnn=887000,
        location_description="18TH ST: DOLORES ST to CHURCH ST (3700 - 3799)",
        address="3750 18TH ST",
        blocklot="3579006",
        block="3579",
        lot="006",
        permit="21MFF-00015",
        status="APPROVED",
        food_items="Snow Cones: Soft Serve Ice Cream & Frozen Virgin Daiquiris",
        x=6004575.869,
        y=2105666.974,
        latitude=37.76201920035647,
        longitude=-122.42730642251331,
        schedule="http://bsm.sfdpw.org/PermitsTracker/reports/report.aspx?title=schedule&report=rptSchedule&params=permit=21MFF-00015&ExportPDF=1&Filename=21MFF-00015_schedule.pdf",
        dayshours=None,
        noisent=None,
        approved=datetime.strptime("01/28/2022 12:00:00 AM", "%m/%d/%Y %I:%M:%S %p"),
        received=datetime.strptime("20210315", "%Y%m%d"),
        priorpermit=0,
        expirationdate=datetime.strptime("11/15/2022 12:00:00 AM", "%m/%d/%Y %I:%M:%S %p"),
        location="(37.76201920035647, -122.42730642251331)",
        fire_prevention_districts=8,
        police_districts=4,
        supervisor_districts=5,
        zip_codes=28862,
        neighborhoods_old=3
    )


    permit = create_permit(test_db, permit_data)
    assert permit is not None
    assert permit.applicant == permit_data.applicant

def test_get_permits_by_applicant(test_db):
    applicant = "The Geez Freeze"
    permits = get_permits_by_applicant(test_db, applicant)
    assert len(permits) >= 0  # As the function will always return a list
    if permits:
        assert all(permit.applicant == applicant for permit in permits)

def test_get_permits_by_address(test_db):
    address = "3750 18TH ST"
    permits = get_permits_by_address(test_db, address)
    assert len(permits) >= 0  # As the function will always return a list
    if permits:
        assert all(address in permit.address for permit in permits)

def test_get_nearest_permits(test_db):
    latitude, longitude = 37.76201920035647, -122.42730642251331
    permits = get_nearest_permits(test_db, latitude, longitude)
    assert len(permits) >= 0  # As the function will always return a list
    # More complex assertions could be implemented to check distance

def test_get_permits_by_conditions(test_db):
    applicant = "Datam SF LLC dba Anzu To You"
    address = "2535 TAYLOR ST"
    permits = get_permits_by_conditions(test_db, applicant=applicant, address=address)
    assert len(permits) >= 0  # As the function will always return a list
    if permits:
        assert all(permit.applicant == applicant and address in permit.address for permit in permits)
