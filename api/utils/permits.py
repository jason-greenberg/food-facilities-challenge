import os
import requests
import csv

from math import radians, cos, sin, asin, sqrt
from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.permit import MobileFoodFacilityPermit
from pydantic_schemas.permit import PermitCreate

POSITIONSTACK_API_KEY = os.getenv('POSITIONSTACK_API_KEY')

# get permit by id
def get_permit(db: Session, permit_id: int):
    return db.query(MobileFoodFacilityPermit).get(permit_id)

# get permits list
def get_permits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MobileFoodFacilityPermit).offset(skip).limit(limit).all()

def log_unresolved_addresses(permit: PermitCreate):
    with open('unresolved_addresses.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([value for value in permit.model_dump().values()])  # write all permit attributes

# create permit
def create_permit(db: Session, permit: PermitCreate):
    # Check if latitude and longitude are provided and are valid
    if not permit.latitude or not permit.longitude:
        # Use positionstack API to get the geocoding data
        address = permit.address
        response = requests.get('http://api.positionstack.com/v1/forward', params={
            'access_key': POSITIONSTACK_API_KEY,
            'query': address,
            'fields': 'latitude,longitude',
        })
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        geocoding_data = response.json()

        if geocoding_data['data']:
            location_data = geocoding_data['data'][0]
            permit.latitude = location_data['latitude']
            permit.longitude = location_data['longitude']
        else:
            # Instead of raising error, log the problem and return None
            log_unresolved_addresses(permit)
            return None

    # Create new permit
    db_permit = MobileFoodFacilityPermit(**permit.dict())
    db.add(db_permit)
    db.commit()
    db.refresh(db_permit)
    return db_permit



# Search by name of applicant with optional "Status" field filter.
def get_permits_by_applicant(db: Session, applicant: str, status: str = None):
    if status:
        return db.query(MobileFoodFacilityPermit).filter(
            and_(
                MobileFoodFacilityPermit.applicant.ilike(f"%{applicant}%"), 
                MobileFoodFacilityPermit.status == status
            )
        ).all()
    else:
        return db.query(MobileFoodFacilityPermit).filter(
            MobileFoodFacilityPermit.applicant.ilike(f"%{applicant}%")
        ).all()

# Search by street name.
def get_permits_by_address(db: Session, address: str):
    return db.query(MobileFoodFacilityPermit).filter(
        MobileFoodFacilityPermit.address.ilike(f"%{address}%")
    ).all()

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

# Now we can use this function to get the nearest permits
def get_nearest_permits(db: Session, latitude: float, longitude: float, status: str = "APPROVED"):
    permits = db.query(MobileFoodFacilityPermit).filter(
        MobileFoodFacilityPermit.status == status
    ).all()

    # convert the lat/lon strings to float
    for permit in permits:
        permit.latitude = float(permit.latitude)
        permit.longitude = float(permit.longitude)
    
    # use the haversine function to calculate distances and get the nearest 5 permits
    permits.sort(key=lambda permit: haversine(longitude, latitude, permit.longitude, permit.latitude))
    return permits[:5]

# Build a query based on multiple conditions
def get_permits_by_conditions(db: Session, applicant: str = None, status: str = None, address: str = None, latitude: float = None, longitude: float = None, default_status: bool = True, skip: int = 0, limit: int = 100):
    # If there is no condition, simply return the permits with the offset and limit.
    if not any([applicant, status, address, latitude, longitude]):
        return get_permits(db=db, skip=skip, limit=limit)
    
    # Start building the query
    query = db.query(MobileFoodFacilityPermit)

    # Add conditions
    if applicant:
        query = query.filter(MobileFoodFacilityPermit.applicant.ilike(f"%{applicant}%"))
    if status:
        query = query.filter(MobileFoodFacilityPermit.status == status)
    elif latitude and longitude and default_status:
        query = query.filter(MobileFoodFacilityPermit.status == "APPROVED")
    if address:
        query = query.filter(MobileFoodFacilityPermit.address.ilike(f"%{address}%"))

    # If there are latitude and longitude, we return nearest permits
    if latitude and longitude:
        permits = query.all()

        # convert the lat/lon strings to float
        for permit in permits:
            permit.latitude = float(permit.latitude)
            permit.longitude = float(permit.longitude)

        # use the haversine function to calculate distances and sort the permits by distance
        permits.sort(key=lambda permit: haversine(longitude, latitude, permit.longitude, permit.latitude))
        
        # Slice the sorted list to only keep the 5 closest ones
        limit = 5
        permits = permits[:limit]

        return permits

    # For all other cases, apply the offset and limit, then execute the query.
    return query.offset(skip).limit(limit).all()
