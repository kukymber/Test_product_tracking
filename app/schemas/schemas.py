from pydantic import BaseModel


class ComponentBase(BaseModel):
    name: str
    quantity: float


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(ComponentBase):
    pass


class Component(ComponentBase):
    id: int

    class Config:
        orm_mode = True
