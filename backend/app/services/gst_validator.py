from decimal import Decimal
from datetime import datetime


VALID_GST_RATES = [
    Decimal("0.05"),
    Decimal("0.12"),
    Decimal("0.18"),
    Decimal("0.28")
]


def validate_gstin(invoice):

    gstin = invoice.get("gstin")

    return gstin is not None


def validate_gst_amount(invoice):

    taxable_amount = Decimal(
        str(invoice.get("taxable_amount", 0))
    )

    extracted_gst = (
        Decimal(str(invoice.get("cgst", 0))) +
        Decimal(str(invoice.get("sgst", 0))) +
        Decimal(str(invoice.get("igst", 0)))
    )

    tolerance = Decimal("2.0")

    for rate in VALID_GST_RATES:

        expected_gst = taxable_amount * rate

        if abs(extracted_gst - expected_gst) <= tolerance:

            return {
                "valid": True,
                "matched_rate": float(rate * 100)
            }

    return {
        "valid": False,
        "matched_rate": None
    }


def validate_invoice_total(invoice):

    taxable_amount = Decimal(
        str(invoice.get("taxable_amount", 0))
    )

    total_gst = (
        Decimal(str(invoice.get("cgst", 0))) +
        Decimal(str(invoice.get("sgst", 0))) +
        Decimal(str(invoice.get("igst", 0)))
    )

    invoice_total = Decimal(
        str(invoice.get("total_amount", 0))
    )

    calculated_total = taxable_amount + total_gst

    tolerance = Decimal("2.0")

    return abs(invoice_total - calculated_total) <= tolerance


def validate_invoice_date(invoice):

    invoice_date = invoice.get("invoice_date")

    if not invoice_date:

        return False

    try:

        parsed_date = datetime.strptime(
            invoice_date,
            "%Y-%m-%d"
        )

        return parsed_date.date() <= datetime.today().date()

    except Exception:

        return False


def validate_invoice(invoice):

    gstin_valid = validate_gstin(invoice)

    gst_validation = validate_gst_amount(invoice)

    total_valid = validate_invoice_total(invoice)

    date_valid = validate_invoice_date(invoice)

    overall_valid = (
        gstin_valid and
        gst_validation["valid"] and
        total_valid and
        date_valid
    )

    return {

        "overall_valid": overall_valid,

        "gstin_valid": gstin_valid,

        "gst_valid": gst_validation["valid"],

        "matched_gst_rate": gst_validation["matched_rate"],

        "total_valid": total_valid,

        "date_valid": date_valid
    }