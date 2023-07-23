from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..db_setup import Base, environment, SCHEMA
from .mixins import Timestamp

class MobileFoodFacilityPermit(Timestamp, Base):
    __tablename__ = "mobile_food_facility_permits"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    applicant = Column(String, nullable=False)
    facility_type = Column(String, nullable=False)
    cnn = Column(Integer, nullable=False)
    location_description = Column(String, nullable=False)
    address = Column(String, nullable=False)
    blocklot = Column(String, nullable=False)
    block = Column(String, nullable=False)
    lot = Column(String, nullable=False)
    permit = Column(String, nullable=False)
    status = Column(String, nullable=False)
    food_items = Column(String, nullable=False)

    location = relationship("Location", back_populates="permits")
