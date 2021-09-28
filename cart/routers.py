from fastapi import APIRouter, Depends , status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from database import get_db
from decimal import Decimal
from accounts.authentication import get_current_user
from accounts.schemas import ShowUser
from product.cruds import get_product_by_id
from .cart import Cart
from . import schemas


router = APIRouter(
    tags=['Cart'],
    prefix='/cart',
)

@router.get('/')
async def get_cart(user: ShowUser = Depends(get_current_user)):

    items = Cart.get_cart(user.id)
    total_price = 0
    for item in items :
        total_price += float(item['price'])
    
    content = {"items":items,"total_price":total_price}
    return JSONResponse(status_code=status.HTTP_200_OK,content=content)


@router.post('/add')
async def add_to_cart(
    request: schemas.AddToCart,
    db: Session = Depends(get_db),
    user: ShowUser = Depends(get_current_user)):

    product = get_product_by_id(db , request.product_id)
    Cart.add_to_cart(
        user_id = user.id,
        product_id = product.id,
        price = str(Decimal(product.price) * request.quantity),
        quantity = request.quantity,
	)
    content = {'message': 'added'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.delete("/clear")
async def clear_cart(user: ShowUser = Depends(get_current_user)):
    Cart.delete_cart(user.id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message":"cart cleared"}
    )


@router.delete('/{product_id}')
async def delete_produt(
    product_id: int,
    user: ShowUser = Depends(get_current_user)):

    Cart.delete_product(user.id,product_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message":"product delted from cart"}
    )



