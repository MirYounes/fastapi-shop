from sqlalchemy import (
    Boolean, Column, Integer,
    String, DateTime, Numeric,
    ForeignKey, Table
)
from sqlalchemy.orm import relationship
import datetime
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    image = Column(String, unique=True)
    price = Column(Numeric)
    available = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime, onupdate=datetime.datetime.now , default=datetime.datetime.now)
    galleries = relationship("Gallery", back_populates="product" , cascade="all, delete")
    items = relationship("OrderItem",back_populates="product")


class Gallery(Base):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="galleries")
