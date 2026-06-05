from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.invoice import Invoice

import pandas as pd

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)


@router.get("/excel")
def export_excel(
    db: Session = Depends(get_db)
):

    invoices = db.query(
        Invoice
    ).all()

    data = []

    for invoice in invoices:

        data.append({

            "Vendor Name": invoice.vendor_name,

            "GSTIN": invoice.gstin,

            "Invoice Number": invoice.invoice_number,

            "Invoice Date": invoice.invoice_date,

            "Taxable Amount": invoice.taxable_amount,

            "CGST": invoice.cgst,

            "SGST": invoice.sgst,

            "IGST": invoice.igst,

            "Total Amount": invoice.total_amount
        })

    df = pd.DataFrame(data)

    file_name = "gst_validation_report.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return FileResponse(

        path=file_name,

        filename=file_name,

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )