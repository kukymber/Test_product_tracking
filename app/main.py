from fastapi import FastAPI
from app.database import engine
from app.models.models import Base
from app.endpoints import components, semiproducts, products, orders, invoices

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(components.router, prefix="/api/v1", tags=["components"])
app.include_router(semiproducts.router, prefix="/api/v1", tags=["semiproducts"])
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
app.include_router(invoices.router, prefix="/api/v1", tags=["invoices"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API"}
