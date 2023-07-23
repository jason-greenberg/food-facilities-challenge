from datetime import datetime
from pydantic import BaseModel

class PermitBase(BaseModel):
    location_id: int
    applicant: str
    facility_type: str
    cnn: int
    location_description: str
    address: str
    blocklot: str
    block: str
    lot: str
    permit: str
    status: str
    food_items: str

class PermitCreate(PermitBase):
    pass

class Permit(PermitBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
