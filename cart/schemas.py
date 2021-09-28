from pydantic import BaseModel


class AddToCart(BaseModel):
    product_id : int
    quantity : int