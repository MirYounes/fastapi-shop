from sqlalchemy.orm import Session
from fastapi import HTTPException , status
from . import models


def get_order(db: Session, id: int):
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="order not fount"
        )
    return order





def create_order(db:Session , user_id , prcie , address):
    order = models.Order(
        customer_id = user_id,
        prcie = int(prcie),
        address = address
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def create_order_item(db:Session,order_id,product_id):
    order_item = models.OrderItem(
        order_id=order_id,
        product_id=product_id
    )
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item