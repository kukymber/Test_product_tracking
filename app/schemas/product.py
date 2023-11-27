from pydantic import BaseModel
from typing import List, Optional

from app.schemas.component import ComponentBase
from app.schemas.semiproduct import SemiProductBase


class ProductBase(BaseModel):
    name: str


class ProductCreate(ProductBase):
    component_ids: Optional[List[int]] = []
    semi_product_ids: Optional[List[int]] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    component_ids: Optional[List[int]] = None
    semi_product_ids: Optional[List[int]] = None


class Product(ProductBase):
    id: int
    components: List[ComponentBase] = []
    semi_products: List[SemiProductBase] = []

    class Config:
        orm_mode = True
