from math import radians, cos, sin, asin, sqrt
from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.permit import MobileFoodFacilityPermit
from pydantic_schemas.permit import PermitCreate

# get permit by id
def get_permit(db: Session, permit_id: int):
    return db.query(MobileFoodFacilityPermit).get(permit_id)

# get permits list
def get_permits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MobileFoodFacilityPermit).offset(skip).limit(limit).all()

# create permit
def create_permit(db: Session, permit: PermitCreate):
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
    permits = db.query(MobileFoodFacilityPermit).join(MobileFoodFacilityPermit.location).filter(
        MobileFoodFacilityPermit.status == status
    ).all()

    # convert the lat/lon strings to float
    for permit in permits:
        permit.location.latitude = float(permit.location.latitude)
        permit.location.longitude = float(permit.location.longitude)
    
    # use the haversine function to calculate distances and get the nearest 5 permits
    permits.sort(key=lambda permit: haversine(longitude, latitude, permit.location.longitude, permit.location.latitude))
    return permits[:5]
