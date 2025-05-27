from datetime import datetime
from pydantic import BaseModel
from app.schemas.product import Product

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    product: Product

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    total: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    items: list[OrderItem]

    class Config:
        from_attributes = True
        