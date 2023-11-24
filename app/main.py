from fastapi import FastAPI
from app.database import engine
from app.models.models import Base
import app.endpoints.components as components
import app.endpoints.semiproducts as semiproducts
import app.endpoints.products as products
import app.endpoints.orders as orders
import app.endpoints.invoices as invoices

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(components.router, prefix="/api/v1", tags=["components"])
# app.include_router(semiproducts.router, prefix="/api/v1", tags=["semiproducts"])
# app.include_router(products.router, prefix="/api/v1", tags=["products"])
# app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
# app.include_router(invoices.router, prefix="/api/v1", tags=["invoices"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}
