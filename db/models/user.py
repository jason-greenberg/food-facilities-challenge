from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text, inspect
from sqlalchemy.orm import relationship
from ..db_setup import Base, SCHEMA, environment
from .mixins import Timestamp

class User(Timestamp, Base):
    __tablename__ = "users"

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    @property
    def password(self):
        return self.hashed_password
    
    @password.setter
    def password(self, password):
        self.hashed_password = password

    def to_dict(self):
        return {c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}
