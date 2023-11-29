from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Invoice as DbInvoice
from app.schemas.invoice import InvoiceCreate, Invoice

router = APIRouter()


@router.post("/invoices/", response_model=Invoice)
def create_invoice(invoice_create: InvoiceCreate, db: Session = Depends(get_db)):
    new_invoice = DbInvoice()

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


@router.get("/invoices/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    pass


