from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Product as DbProduct, Component as DbComponent, SemiProduct as DbSemiProduct
from app.schemas.product import ProductCreate, ProductUpdate, Product

router = APIRouter()

@router.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        products = db.query(DbProduct).offset(skip).limit(limit).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/products/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = DbProduct(name=product.name)

    if product.component_ids:
        components = db.query(DbComponent).filter(DbComponent.id.in_(product.component_ids)).all()
        new_product.components = components

    if product.semi_product_ids:
        semi_products = db.query(DbSemiProduct).filter(DbSemiProduct.id.in_(product.semi_product_ids)).all()
        new_product.semi_products = semi_products

    db.add(new_product)
    try:
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(DbProduct).filter(DbProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.name:
        db_product.name = product.name

    if product.component_ids is not None:
        current_component_ids = set(db_product.components)
        new_component_ids = set(product.component_ids)
        for component_id in new_component_ids - current_component_ids:
            component = db.query(DbComponent).filter(DbComponent.id == component_id).first()
            if component:
                db_product.components.append(component)

    if product.semi_product_ids is not None:
        current_semi_product_ids = set(db_product.semi_products)
        new_semi_product_ids = set(product.semi_product_ids)
        for semi_product_id in new_semi_product_ids - current_semi_product_ids:
            semi_product = db.query(DbSemiProduct).filter(DbSemiProduct.id == semi_product_id).first()
            if semi_product:
                db_product.semi_products.append(semi_product)

    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(DbProduct).filter(DbProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    try:
        db.commit()
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
