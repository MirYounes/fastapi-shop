from pydantic import BaseModel
from typing import List
import datetime


class AdminProdcutList(BaseModel):
    id : int
    title : str
    price : int
    available : bool

    class Config:
        orm_mode = True

class Galleries(BaseModel):
    image : str

    class Config:
        orm_mode = True


class AdminProductDetail(BaseModel):
    id : int
    title: str 
    description: str
    image: str 
    price: float 
    available : bool
    galleries : List[Galleries]
    #updated : datetime.datetime
    created : datetime.datetime

    class Config:
        orm_mode = True




