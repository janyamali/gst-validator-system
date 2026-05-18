from app.models.invoice import Invoice


def detect_duplicate(db, parsed_invoice):

    existing_invoice = db.query(Invoice).filter(

        Invoice.invoice_number ==
        parsed_invoice["invoice_number"],

        Invoice.vendor_name ==
        parsed_invoice["vendor_name"],

        Invoice.total_amount ==
        parsed_invoice["total_amount"]

    ).first()

    return existing_invoice is not None