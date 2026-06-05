from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.invoice import Invoice
from app.api.routes.invoices import router as invoices_router


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.get("/")
def get_invoices(
    db: Session = Depends(get_db)
):

    invoices = db.query(
        Invoice
    ).all()

    return [

        {

            "id": str(invoice.id),

            "vendor_name": invoice.vendor_name,

            "gstin": invoice.gstin,

            "invoice_number": invoice.invoice_number,

            "invoice_date": str(
                invoice.invoice_date
            ),

            "taxable_amount": float(
                invoice.taxable_amount
            ),

            "cgst": float(
                invoice.cgst
            ),

            "sgst": float(
                invoice.sgst
            ),

            "igst": float(
                invoice.igst
            ),

            "total_amount": float(
                invoice.total_amount
            )
        }

        for invoice in invoices
    ]