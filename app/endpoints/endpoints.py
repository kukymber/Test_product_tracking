from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database.py import get_db
from models.py import Component
from schemas import ComponentCreate, ComponentUpdate

router = APIRouter()

@router.get("/components/", response_model=List[Component])
def read_components(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    components = db.query(Component).offset(skip).limit(limit).all()
    return components

@router.post("/components/", response_model=Component)
def create_component(component: ComponentCreate, db: Session = Depends(get_db)):
    db_component = Component(name=component.name, quantity=component.quantity)
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component

@router.put("/components/{component_id}", response_model=Component)
def update_component(component_id: int, component: ComponentUpdate, db: Session = Depends(get_db)):
    db_component = db.query(Component).filter(Component.id == component_id).first()
    if db_component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    for key, value in component.dict().items():
        setattr(db_component, key, value)
    db.commit()
    db.refresh(db_component)
    return db_component

@router.delete("/components/{component_id}", response_model=Component)
def delete_component(component_id: int, db: Session = Depends(get_db)):
    db_component = db.query(Component).filter(Component.id == component_id).first()
    if db_component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    db.delete(db_component)
    db.commit()
    return db_component
