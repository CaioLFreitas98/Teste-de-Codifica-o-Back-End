from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.db.models.order import OrderStatus

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    client_id: int
    items: List[OrderItemCreate]

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderOut(BaseModel):
    id: int
    client_id: int
    user_id: int
    status: OrderStatus
    total_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
