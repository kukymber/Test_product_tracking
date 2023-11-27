from pydantic import BaseModel
from typing import List, Union, Optional
from app.schemas.component import Component



class SemiProductBase(BaseModel):
    name: str


class SemiProductCreate(SemiProductBase):
    component_ids: List[int]


class SemiProductUpdate(BaseModel):
    name: Union[str, None] = None
    component_ids: Optional[List[int]]


class SemiProduct(SemiProductBase):
    id: int
    name: str
    components: List[Component]

    class Config:
        from_attributes = True
