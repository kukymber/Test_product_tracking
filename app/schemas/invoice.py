from pydantic import BaseModel
from typing import List


class InvoiceItem(BaseModel):
    component_id: int
    quantity: int


class InvoiceCreate(BaseModel):
    items: List[InvoiceItem]


class Invoice(BaseModel):
    id: int
    items: List[InvoiceItem]

    class Config:
        from_attributes = True
