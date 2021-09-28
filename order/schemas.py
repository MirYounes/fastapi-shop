from typing import List
from pydantic import BaseModel
from typing import List


class OrderCreate(BaseModel):
    address : str

    
class OrderList(BaseModel):
    id : int
    paid : bool
    price : int

    class Config:
        orm_mode = True


class OrderItemList(BaseModel):
    product_id : int
    order_id : int

    class Config:
        orm_mode = True


class OrderDetail(BaseModel):
    id : int
    paid : bool
    price : int
    address : str
    items : List[OrderItemList]    

    class Config:
        orm_mode = True