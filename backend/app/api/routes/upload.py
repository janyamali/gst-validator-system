from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from datetime import datetime

from app.core.database import get_db

from app.models.invoice import Invoice
from app.models.validation import Validation

# from app.services.azure_ocr import analyze_invoice
from app.services.local_ocr import analyze_invoice
# from app.services.paddle_ocr import analyze_invoice

from app.services.invoice_parser import parse_invoice_data

from app.services.gst_validator import validate_invoice

from app.services.duplicate_detector import detect_duplicate

from app.services.matcher import match_claim_with_invoice

from fastapi import Form


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_invoice(

    file: UploadFile = File(...),

    employee_name: str = Form(...),

    claim_number: str = Form(...),

    claimed_amount: float = Form(...),

    claimed_gst: float = Form(...),

    vendor_name: str = Form(...),

    invoice_number: str = Form(...),

    db: Session = Depends(get_db)
):

    # READ FILE
    content = await file.read()

    # OCR EXTRACTION
    raw_invoices = analyze_invoice(content)

    processed_invoices = []

    for invoice in raw_invoices:

        # STEP 1 — PARSE INVOICE
        parsed_invoice = parse_invoice_data(invoice)

        # STEP 2 — DUPLICATE DETECTION
        duplicate_detected = detect_duplicate(
            db,
            parsed_invoice
        )

        # STEP 3 — GST VALIDATION
        validation_result = validate_invoice(
            parsed_invoice
        )

        # STEP 4 — CLAIM DATA
        claim_data = {

    "employee_name": employee_name,

    "claim_number": claim_number,

    "claimed_amount": claimed_amount,

    "claimed_gst": claimed_gst,

    "vendor_name": vendor_name,

    "invoice_number": invoice_number
}

        # STEP 5 — CLAIM MATCHING
        match_result = match_claim_with_invoice(

            claim_data,

            parsed_invoice
        )

        # STEP 6 — SAVE INVOICE
        invoice_record = Invoice(

            vendor_name=parsed_invoice["vendor_name"],

            gstin=parsed_invoice["gstin"],

            invoice_number=parsed_invoice["invoice_number"],

            invoice_date=datetime.strptime(
                parsed_invoice["invoice_date"],
                "%Y-%m-%d"
            ).date(),

            taxable_amount=parsed_invoice["taxable_amount"],

            cgst=parsed_invoice["cgst"],

            sgst=parsed_invoice["sgst"],

            igst=parsed_invoice["igst"],

            total_amount=parsed_invoice["total_amount"]
        )

        db.add(invoice_record)

        db.commit()

        db.refresh(invoice_record)

        # STEP 7 — SAVE VALIDATION RESULT
        validation_record = Validation(

            invoice_id=invoice_record.id,

            status=(
                "VALID"
                if validation_result["overall_valid"]
                else "INVALID"
            ),

            remarks="GST Validation Completed",

            validated_gst=(
                parsed_invoice["cgst"] +
                parsed_invoice["sgst"] +
                parsed_invoice["igst"]
            ),

            mismatch_amount=0,

            duplicate_detected=duplicate_detected
        )

        db.add(validation_record)

        db.commit()

        # STEP 8 — FINAL RESPONSE
        processed_invoices.append({

            "parsed_invoice": parsed_invoice,

            "validation": validation_result,

            "duplicate_detected": duplicate_detected,

            "claim_match": match_result
        })

    return {

        "success": True,

        "data": processed_invoices
    }