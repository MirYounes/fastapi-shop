from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from product import schemas , cruds
from database import get_db


router = APIRouter(
    tags=['Products'],
    prefix='/products',
    #dependencies=[Depends(get_current_user_admin)],
)


@router.get('/', response_model=List[schemas.AdminProdcutList])
async def get_products(db:Session=Depends(get_db), skip:Optional[int]=0,limit:Optional[int]=100):
    return cruds.get_products(db, skip , limit)


@router.get('/{id}', response_model=schemas.AdminProductDetail)
async def get_product(id:int,db:Session=Depends(get_db)):
    return cruds.get_product_by_id(db,id)
