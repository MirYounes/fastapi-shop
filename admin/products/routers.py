from typing import List, Optional
from fastapi import APIRouter, Depends, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from accounts.authentication import get_current_user_admin
from starlette.responses import JSONResponse
from product import schemas , cruds
from database import get_db


router = APIRouter(
    tags=['Admin Products'],
    prefix='/admin/products',
    #dependencies=[Depends(get_current_user_admin)],
)


@router.get('/', response_model=List[schemas.AdminProdcutList])
async def get_products(db:Session=Depends(get_db), skip:Optional[int]=0,limit:Optional[int]=100):
    return cruds.get_products(db, skip , limit)


@router.get('/{id}', response_model=schemas.AdminProductDetail)
async def get_product(id:int,db:Session=Depends(get_db)):
    return cruds.get_product_by_id(db,id)


@router.post('/create')
async def create(
    db : Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = Form(...),
    price: float = Form(...), 
    galleries: List[UploadFile] = File(...)
                ):
  
    await cruds.create(db,title,description,image,price,galleries)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED
        , content={"message":"product created"}
        )

@router.put('/{id}')
async def update(
    id: int,
    db:Session=Depends(get_db),
    title: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    available : Optional[bool] = None,
    image: UploadFile = File(None)
    ):
    await cruds.update(id,db,title,description,price,available,image)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED
        , content={"message":"product updated"}
        )

@router.delete('/{id}')
async def delete_product(id:int,db:Session=Depends(get_db)):
    cruds.delete_product(id , db)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message":"product deleted"}
        )
