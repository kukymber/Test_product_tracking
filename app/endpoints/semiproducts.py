from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import SemiProduct, Component
from app.schemas.semiproduct import SemiProductCreate, SemiProductUpdate, SemiProductBase

router = APIRouter()


@router.get("/semiproducts/", response_model=List[SemiProductBase])
def read_semiproducts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        semiproducts = db.query(SemiProduct).offset(skip).limit(limit).all()
        return semiproducts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/semiproducts/", response_model=SemiProductBase)
def create_semiproduct(semiproduct: SemiProductCreate, db: Session = Depends(get_db)):
    new_semiproduct = SemiProduct(**semiproduct.dict())
    db.add(new_semiproduct)
    try:
        db.commit()
        db.refresh(new_semiproduct)
        return new_semiproduct
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/semiproducts/{semiproduct_id}", response_model=SemiProductBase)
def update_semiproduct(semiproduct_id: int, semiproduct: SemiProductUpdate, db: Session = Depends(get_db)):
    db_semiproduct = db.query(SemiProduct).filter(SemiProduct.id == semiproduct_id).first()
    if db_semiproduct is None:
        raise HTTPException(status_code=404, detail="SemiProduct not found")

    if semiproduct.name is not None:
        db_semiproduct.name = semiproduct.name

    if semiproduct.component_ids is not None:
        current_component_ids = {component.id for component in db_semiproduct.components}
        new_component_ids = set(semiproduct.component_ids)

        for component in db_semiproduct.components:
            if component.id not in new_component_ids:
                db_semiproduct.components.remove(component)

        for component_id in new_component_ids - current_component_ids:
            component = db.query(Component).filter(Component.id == component_id).first()
            if component:
                db_semiproduct.components.append(component)

    try:
        db.commit()
        db.refresh(db_semiproduct)
        return db_semiproduct
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/semiproducts/{semiproduct_id}", response_model=SemiProductBase)
def delete_semiproduct(semiproduct_id: int, db: Session = Depends(get_db)):
    db_semiproduct = db.query(SemiProduct).filter(SemiProduct.id == semiproduct_id).first()
    if db_semiproduct is None:
        raise HTTPException(status_code=404, detail="SemiProduct not found")
    try:
        db.delete(db_semiproduct)
        db.commit()
        return db_semiproduct
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
