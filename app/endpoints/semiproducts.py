from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import SemiProduct as DbSemiProduct, Component as DbComponent
from app.schemas.semiproduct import SemiProductCreate, SemiProductUpdate, SemiProduct, SemiProductBase

router = APIRouter()


# Используем модель Pydantic для ответа
@router.get("/semiproducts/", response_model=List[SemiProduct])
def read_semiproducts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        semiproducts = db.query(DbSemiProduct).offset(skip).limit(limit).all()
        return semiproducts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/semiproducts/", response_model=SemiProduct)
def create_semiproduct(semiproduct: SemiProductCreate, db: Session = Depends(get_db)):
    new_semiproduct = DbSemiProduct(name=semiproduct.name)

    if semiproduct.component_ids:
        components = db.query(DbComponent).filter(DbComponent.id.in_(semiproduct.component_ids)).all()
        new_semiproduct.components = components

    db.add(new_semiproduct)
    try:
        db.commit()
        db.refresh(new_semiproduct)
        return new_semiproduct
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/semiproducts/{semiproduct_id}", response_model=SemiProduct)
def update_semiproduct(semiproduct_id: int, semiproduct: SemiProductUpdate, db: Session = Depends(get_db)):
    db_semiproduct = db.query(DbSemiProduct).filter(DbSemiProduct.id == semiproduct_id).first()
    if db_semiproduct is None:
        raise HTTPException(status_code=404, detail="SemiProduct not found")

    if semiproduct.name:
        db_semiproduct.name = semiproduct.name

    if semiproduct.component_ids is not None:
        current_component_ids = {component.id for component in db_semiproduct.components}
        new_component_ids = set(semiproduct.component_ids)

        # Обновление списка компонентов
        for component_id in new_component_ids - current_component_ids:
            component = db.query(DbComponent).filter(DbComponent.id == component_id).first()
            if component:
                db_semiproduct.components.append(component)

        db_semiproduct.components = [component for component in db_semiproduct.components if
                                     component.id in new_component_ids]

    try:
        db.commit()
        db.refresh(db_semiproduct)
        return db_semiproduct
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/semiproducts/{semiproduct_id}", response_model=SemiProductBase)
def delete_semiproduct(semiproduct_id: int, db: Session = Depends(get_db)):
    db_semiproduct = db.query(DbSemiProduct).filter(DbSemiProduct.id == semiproduct_id).first()
    if db_semiproduct is None:
        raise HTTPException(status_code=404, detail="SemiProduct not found")
    try:
        db.delete(db_semiproduct)
        db.commit()
        return db_semiproduct
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
