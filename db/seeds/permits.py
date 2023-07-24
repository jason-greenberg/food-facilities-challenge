from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from db.models.permit import MobileFoodFacilityPermit
from db.db_setup import environment, SCHEMA
from api.utils.permits import create_permit
from pydantic_schemas.permit import PermitCreate

import os
import csv
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'Mobile_Food_Facility_Permit.csv')

def seed_permits(db: Session):
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            # Convert date strings to datetime objects
            approved = datetime.strptime(row[19], '%m/%d/%Y %I:%M:%S %p') if row[19] else None
            
            # Convert received to datetime object if it's not empty or 0
            received = datetime.strptime(row[20], '%Y%m%d') if row[20] not in ['', '0'] else None

            # Convert expirationdate to datetime object if it's not empty
            expiration_date = datetime.strptime(row[22], '%m/%d/%Y %I:%M:%S %p') if row[22] else None

            # Convert NOISent to datetime object if it's not empty
            noisent = datetime.strptime(row[18], '%m/%d/%Y %I:%M:%S %p') if row[18] else None

            # Convert prior_permit to Boolean
            prior_permit = True if row[21] == '1' else False

            # Handle instances where X or Y does not represent a float
            try:
                x = float(row[12])
            except ValueError:
                x = None

            try:
                y = float(row[13])
            except ValueError:
                y = None

            # Create the PermitCreate instance
            permit_create = PermitCreate(
                location_id=int(row[0]),
                applicant=row[1],
                facility_type=row[2],
                cnn=int(row[3]),
                location_description=row[4],
                address=row[5],
                blocklot=row[6],
                block=row[7],
                lot=row[8],
                permit=row[9],
                status=row[10],
                food_items=row[11],
                x=x,
                y=y,
                latitude=float(row[14]),
                longitude=float(row[15]),
                schedule=row[16],
                dayshours=row[17],
                noisent=noisent,
                approved=approved,
                received=received,
                priorpermit=prior_permit,
                expirationdate=expiration_date,
                location=row[23],
                fire_prevention_districts=int(row[24]) if row[24] else None,
                police_districts=int(row[25]) if row[25] else None,
                supervisor_districts=int(row[26]) if row[26] else None,
                zip_codes=int(row[27]) if row[27] else None,
                neighborhoods_old=int(row[28]) if row[28] else None,
            )

            # Create the permit and skip if None
            permit = create_permit(db=db, permit=permit_create)
            if permit is None:
                continue



def undo_permits(db: Session):
    if environment == "production":
        db.execute(f"TRUNCATE table {SCHEMA}.mobile_food_facility_permits RESTART IDENTITY CASCADE;")
    else:
        db.execute(text("DELETE FROM mobile_food_facility_permits"))
