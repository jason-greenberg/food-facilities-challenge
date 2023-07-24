from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PermitBase(BaseModel):
    location_id: int
    applicant: str
    facility_type: str
    cnn: int
    location_description: Optional[str]
    address: str
    blocklot: Optional[str]
    block: Optional[str]
    lot: Optional[str]
    permit: str
    status: str
    food_items: Optional[str]
    x: Optional[float]
    y: Optional[float]
    latitude: float
    longitude: float
    schedule: Optional[str]
    dayshours: Optional[str]
    noisent: Optional[datetime]
    approved: Optional[datetime]
    received: str
    priorpermit: bool
    expirationdate: Optional[datetime]
    location: Optional[str]
    fire_prevention_districts: Optional[int]
    police_districts: Optional[int]
    supervisor_districts: Optional[int]
    zip_codes: Optional[int]
    neighborhoods_old: Optional[int]

class PermitCreate(PermitBase):
    pass

class Permit(PermitBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
