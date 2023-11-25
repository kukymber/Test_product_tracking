from pydantic import BaseModel
from typing import Union


class ComponentBase(BaseModel):
    id: int
    name: str
    quantity: float


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(ComponentBase):
    name: Union[str, None] = None
    quantity: Union[float, None] = None


class Component(ComponentBase):
    id: int

    class Config:
        from_attributes = True
