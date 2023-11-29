from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order as DbOrder, Product as DbProduct, Component as DbComponent
from app.schemas.order import OrderCreate, Order

router = APIRouter()


@router.post("/orders/", response_model=Order)
def create_order(order_create: OrderCreate, db: Session = Depends(get_db)):
    new_order = DbOrder()
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order_create.items:
        product = db.query(DbProduct).filter(DbProduct.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")

        for component in product.components:
            component.quantity -= item.quantity
            db.add(component)

        for semi_product in product.semi_products:
            for component in semi_product.components:
                component.quantity -= item.quantity
                db.add(component)

        new_order.products.append(product)

    db.commit()
    return new_order


@router.get("/orders/", response_model=List[Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(DbOrder).offset(skip).limit(limit).all()
    return orders


@router.delete("/orders/{order_id}", response_model=Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(DbOrder).filter(DbOrder.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(db_order)
    db.commit()
    return db_order
