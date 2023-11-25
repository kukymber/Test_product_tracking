from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Component
from app.schemas.component import ComponentCreate, ComponentUpdate, ComponentCreate, ComponentBase

router = APIRouter()


@router.get("/components/", response_model=List[ComponentBase])
def read_components(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        components = db.query(Component).offset(skip).limit(limit).all()
        return components
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/components/", response_model=ComponentCreate)
def create_component(component: ComponentCreate, db: Session = Depends(get_db)):
    db_component = Component(**component.dict())
    db.add(db_component)
    try:
        db.commit()
        db.refresh(db_component)
        return db_component
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/components/{component_id}", response_model=ComponentBase)
def update_component(component_id: int, component: ComponentUpdate, db: Session = Depends(get_db)):
    db_component = db.query(Component).filter(Component.id == component_id).first()
    if db_component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    try:
        for key, value in component.dict(exclude_unset=True).items():
            setattr(db_component, key, value)
        db.commit()
        db.refresh(db_component)
        return db_component
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/components/{component_id}", response_model=ComponentBase)
def delete_component(component_id: int, db: Session = Depends(get_db)):
    db_component = db.query(Component).filter(Component.id == component_id).first()
    if db_component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    try:
        db.delete(db_component)
        db.commit()
        return db_component
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
