from fastapi import APIRouter, Depends , status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from database import get_db
from accounts.schemas import ShowUser
from accounts.authentication import get_current_user
from cart.cart import Cart
from . import cruds , schemas


router = APIRouter(
    tags=['Orders'],
    prefix='/orders',
)


@router.get('', response_model=schemas.OrderList)
async def get_orders(user: ShowUser = Depends(get_current_user)):
    return user.orders


@router.get('/{id}', response_model=schemas.OrderDetail)
async def get_orders(id:int,user: ShowUser = Depends(get_current_user),db:Session=Depends(get_db) ):
    return cruds.get_order(db,id)


@router.post('/create')
async def create_order(request:schemas.OrderCreate,user: ShowUser = Depends(get_current_user),db:Session=Depends(get_db)):
    items = Cart.get_cart(user.id)
    if items == None :
        return None
        
    total_price = 0
    for item in items:
        total_price += float(item['price'])
    order = cruds.create_order(db,user.id,total_price,request.address)

    for item in items:
        order_item = cruds.create_order_item(db,order.id,float(item["product_id"]))
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message":"order created"}
    )
