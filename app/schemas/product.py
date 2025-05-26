from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class ProductBase(BaseModel):
    description: str = Field(..., max_length=255)
    sale_price: float
    barcode: str = Field(..., max_length=50)
    section: str = Field(..., max_length=50)
    initial_stock: int
    expiration_date: Optional[date] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    description: Optional[str] = Field(None, max_length=255)
    sale_price: Optional[float] = None
    barcode: Optional[str] = Field(None, max_length=50)
    section: Optional[str] = Field(None, max_length=50)
    initial_stock: Optional[int] = None
    expiration_date: Optional[date] = None
    image_url: Optional[str] = None

class ProductOut(ProductBase):
    id: int
    current_stock: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
