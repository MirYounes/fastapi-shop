from sqlalchemy import (
    Boolean, Column, Integer,
    String, DateTime, Numeric,
    ForeignKey,Float
)
from sqlalchemy.orm import relationship
import datetime
from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    customer = relationship("User", back_populates="orders")
    price = Column(Float)
    paid = Column(Boolean, default=False)
    address = Column(String)
    created = Column(DateTime, default=datetime.datetime.now())
    items = relationship("OrderItem",back_populates="order",cascade="all, delete")


class OrderItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order",back_populates="items")
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product",back_populates="items")
