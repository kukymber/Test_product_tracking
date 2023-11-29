from pydantic import BaseModel
from typing import List, Optional, Dict


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    pass


class Order(BaseModel):
    items: Optional[List[OrderItem]]

    class Config:
        from_attributes = True
