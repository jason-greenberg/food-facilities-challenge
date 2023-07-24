from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, inspect
from sqlalchemy.orm import relationship
from ..db_setup import Base, environment, SCHEMA
from .mixins import Timestamp

class MobileFoodFacilityPermit(Timestamp, Base):
    __tablename__ = "mobile_food_facility_permits"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, nullable=False)
    applicant = Column(String, nullable=False)
    facility_type = Column(String, nullable=False)
    cnn = Column(Integer, nullable=False)
    location_description = Column(String, nullable=True)
    address = Column(String, nullable=False)
    blocklot = Column(String, nullable=True)
    block = Column(String, nullable=True)
    lot = Column(String, nullable=True)
    permit = Column(String, nullable=False)
    status = Column(String, nullable=False)
    food_items = Column(String, nullable=True)
    x = Column(Float, nullable=True)
    y = Column(Float, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    schedule = Column(String, nullable=True)
    dayshours = Column(String, nullable=True)
    noisent = Column(DateTime, nullable=True)
    approved = Column(DateTime, nullable=True)
    received = Column(String, nullable=False)
    priorpermit = Column(Boolean, nullable=False)
    expirationdate = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    fire_prevention_districts = Column(Integer, nullable=True)
    police_districts = Column(Integer, nullable=True)
    supervisor_districts = Column(Integer, nullable=True)
    zip_codes = Column(Integer, nullable=True)
    neighborhoods_old = Column(Integer, nullable=True)

    def to_dict(self):
        return {c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}
