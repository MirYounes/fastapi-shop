from sqlalchemy import (
    Boolean, Column, Integer, String, DateTime
)
from sqlalchemy.orm import relationship
import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    full_name = Column(String)
    date_joined = Column(DateTime, default=datetime.datetime.now)
    orders = relationship("Order", back_populates="customer" , cascade="all, delete")
