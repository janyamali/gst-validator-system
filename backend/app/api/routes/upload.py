from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db

from app.models.invoice import Invoice
from app.models.validation import Validation

from app.services.local_ocr import analyze_invoice
from app.services.invoice_parser import parse_invoice_data
from app.services.gst_validator import validate_invoice
from app.services.duplicate_detector import detect_duplicate
from app.services.matcher import match_claim_with_invoice
from app.services.ai_reasoning import generate_reason

from app.services.excel_parser import (
    load_claims_excel,
    find_claim_by_invoice_number
)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_invoice(

    invoice_pdfs: List[UploadFile] = File(...),

    claims_excel: UploadFile = File(...),

    db: Session = Depends(get_db)

):

    print("\n" + "=" * 80)
    print(f"TOTAL PDFs RECEIVED: {len(invoice_pdfs)}")
    print("=" * 80)

    for pdf in invoice_pdfs:
        print(f"PDF RECEIVED: {pdf.filename}")

    excel_content = await claims_excel.read()

    claims_df = load_claims_excel(
        excel_content
    )

    processed_invoices = []

    for index, invoice_pdf in enumerate(invoice_pdfs, start=1):

        print("\n" + "=" * 80)
        print(f"PROCESSING PDF {index}/{len(invoice_pdfs)}")
        print(f"FILE NAME : {invoice_pdf.filename}")
        print("=" * 80)

        try:

            pdf_content = await invoice_pdf.read()

            raw_invoice = analyze_invoice(
                pdf_content
            )

            print("\nOCR RETURN TYPE:")
            print(type(raw_invoice))

            if isinstance(raw_invoice, dict):

                print(raw_invoice.keys())

            else:

                print(raw_invoice)

            parsed_invoice = parse_invoice_data(
                raw_invoice
            )

            claim_data = find_claim_by_invoice_number(

                parsed_invoice["invoice_number"],

                claims_df

            )

            print("\nNORMALIZED CLAIM DATA:")
            print(claim_data)

            if claim_data is None:

                processed_invoices.append({

                    "file": invoice_pdf.filename,

                    "error":
                    "Invoice Number not found in Excel",

                    "invoice_number":
                    parsed_invoice["invoice_number"]

                })

                continue

            duplicate_detected = detect_duplicate(

                db,

                parsed_invoice

            )

            validation_result = validate_invoice(

                parsed_invoice

            )

            match_result = match_claim_with_invoice(

                claim_data,

                parsed_invoice

            )

            final_status = (

                "VALID"

                if (

                    validation_result["overall_valid"]

                    and

                    match_result["overall_match"]

                    and

                    not duplicate_detected

                )

                else

                "INVALID"

            )

            ai_reason = generate_reason(

                validation_result,

                match_result,

                duplicate_detected,

                final_status

            )

            print("\n========== AI REASON ==========")
            print(ai_reason)
            print("===============================")

            invoice_date = datetime.strptime(

                parsed_invoice["invoice_date"],

                "%Y-%m-%d"

            ).date()

            invoice_record = Invoice(

                claim_voucher_number=
                parsed_invoice["claim_voucher_number"],

                vendor_name=
                parsed_invoice["vendor_name"],

                gstin=
                parsed_invoice["gstin"],

                invoice_number=
                parsed_invoice["invoice_number"],

                invoice_date=
                invoice_date,

                taxable_amount=
                parsed_invoice["taxable_amount"],

                cgst=
                parsed_invoice["cgst"],

                sgst=
                parsed_invoice["sgst"],

                igst=
                parsed_invoice["igst"],

                total_amount=
                parsed_invoice["total_amount"],

                claimed_amount=
                claim_data["claimed_amount"],

                claimed_gst=
                claim_data["claimed_gst"],

                validation_status=
                final_status

            )

            db.add(invoice_record)

            db.commit()

            db.refresh(invoice_record)

            validation_record = Validation(

                invoice_id=
                invoice_record.id,

                status=
                final_status,

                remarks=
                "Validation Completed",

                validated_gst=(

                    parsed_invoice["cgst"]

                    +

                    parsed_invoice["sgst"]

                    +

                    parsed_invoice["igst"]

                ),

                mismatch_amount=

                abs(

                    float(

                        claim_data.get(
                            "claimed_amount",
                            0
                        )

                    )

                    -

                    float(

                        parsed_invoice.get(
                            "total_amount",
                            0
                        )

                    )

                ),

                duplicate_detected=
                duplicate_detected,

                voucher_match=False,

                vendor_match=
                match_result["vendor_match"],

                invoice_match=
                match_result["invoice_number_match"],

                amount_match=
                match_result["amount_match"],

                gst_match=
                match_result["gst_match"]

            )

            db.add(validation_record)

            db.commit()

            processed_invoices.append({

                "file":
                invoice_pdf.filename,

                "claim_data":
                claim_data,

                "parsed_invoice":
                parsed_invoice,

                "validation":
                validation_result,

                "duplicate_detected":
                duplicate_detected,

                "claim_match":
                match_result,

                "status":
                final_status,

                "ai_reason":
                ai_reason

            })

        except Exception as e:

            print("\nERROR PROCESSING PDF:")
            print(invoice_pdf.filename)
            print(str(e))

            processed_invoices.append({

                "file":
                invoice_pdf.filename,

                "error":
                str(e)

            })

    print("\n" + "=" * 80)
    print(f"TOTAL RESULTS RETURNED : {len(processed_invoices)}")
    print("=" * 80)

    return {

        "success": True,

        "count": len(processed_invoices),

        "data": processed_invoices

    }