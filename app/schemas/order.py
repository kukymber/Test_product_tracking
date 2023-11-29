from pydantic import BaseModel
from typing import List, Dict


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItem]


class Order(BaseModel):
    id: int
    items: List[OrderItem]

    class Config:
        orm_mode = True
