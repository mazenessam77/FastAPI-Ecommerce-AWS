from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CheckoutItem(BaseModel):
    product_id: int
    quantity: int


class CheckoutRequest(BaseModel):
    items: List[CheckoutItem]


class OrderItemOut(BaseModel):
    id: int
    product_id: Optional[int]
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    order_items: List[OrderItemOut]

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    message: str
    data: OrderOut


class OrdersListResponse(BaseModel):
    message: str
    data: List[OrderOut]
