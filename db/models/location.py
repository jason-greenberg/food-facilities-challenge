from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..db_setup import Base
from .mixins import Timestamp

class Location(Timestamp, Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)

    permits = relationship("MobileFoodFacilityPermit", back_populates="location")
