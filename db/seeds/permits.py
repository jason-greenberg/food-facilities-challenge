from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from db.models.permit import MobileFoodFacilityPermit
from db.db_setup import environment, SCHEMA
from api.utils.permits import create_permit
from pydantic_schemas.permit import PermitCreate

import csv
from datetime import datetime

def seed_permits(db: Session):
    with open('mobile_food_facility_permit.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            # Convert date strings to datetime objects
            approved = datetime.strptime(row[19], '%m/%d/%Y %I:%M:%S %p')
            received = datetime.strptime(row[21], '%Y%m%d')
            expiration_date = datetime.strptime(row[23], '%m/%d/%Y %I:%M:%S %p')

            # Create the PermitCreate instance
            permit_create = PermitCreate(
                location_id=row[0],
                applicant=row[1],
                facility_type=row[2],
                cnn=row[3],
                location_description=row[4],
                address=row[5],
                blocklot=row[6],
                block=row[7],
                lot=row[8],
                permit=row[9],
                status=row[10],
                food_items=row[11],
                x=row[12],
                y=row[13],
                schedule=row[16],
                NOISent=row[18],
                approved=approved,
                received=received,
                prior_permit=row[22],
                expiration_date=expiration_date,
            )

            # Create the permit
            create_permit(db=db, permit=permit_create)

def undo_permits(db: Session):
    if environment == "production":
        db.execute(f"TRUNCATE table {SCHEMA}.mobile_food_facility_permits RESTART IDENTITY CASCADE;")
    else:
        db.execute(text("DELETE FROM mobile_food_facility_permits"))
