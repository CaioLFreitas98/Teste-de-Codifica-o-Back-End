from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    cpf: str = Field(..., min_length=11, max_length=11) 
    phone: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = Field(None, min_length=11, max_length=11)
    phone: Optional[str] = None

class ClientOut(ClientBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
