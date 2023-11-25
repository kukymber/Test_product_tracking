from pydantic import BaseModel
from typing import List, Union, Optional


class SemiProductBase(BaseModel):
    name: str


class SemiProductCreate(SemiProductBase):
    component_ids: List[int]  # Список ID компонентов


class SemiProductUpdate(BaseModel):
    name: Union[str, None] = None
    component_ids: Union[List[int], None] = None


class SemiProduct(SemiProductBase):
    id: int
    components: List[Component] = []  # Список компонентов

    class Config:
        from_attributes = True
