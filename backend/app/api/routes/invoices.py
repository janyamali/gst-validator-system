from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.invoice import Invoice



router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.get("/")
#invoices endpoint
def get_invoices(
    db: Session = Depends(get_db)
):

    invoices = db.query(
        Invoice
    ).all()

    return [

    {

        "id": str(invoice.id),

        "claim_voucher_number":
        invoice.claim_voucher_number,

        "vendor_name":
        invoice.vendor_name,

        "gstin":
        invoice.gstin,

        "invoice_number":
        invoice.invoice_number,

        "invoice_date":
        str(invoice.invoice_date),

        "taxable_amount":
        float(invoice.taxable_amount),

        "cgst":
        float(invoice.cgst),

        "sgst":
        float(invoice.sgst),

        "igst":
        float(invoice.igst),

        "total_amount":
        float(invoice.total_amount),

        "claimed_amount":
        float(invoice.claimed_amount),

        "claimed_gst":
        float(invoice.claimed_gst),

        "validation_status":
        invoice.validation_status
    }

    for invoice in invoices
]