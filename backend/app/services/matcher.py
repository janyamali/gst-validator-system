def match_claim_with_invoice(
    claim,
    invoice
):

    amount_match = (

        abs(
            float(claim["claimed_amount"]) -
            float(invoice["total_amount"])
        ) <= 2

    )

    vendor_match = (

        claim["vendor_name"]
        .strip()
        .lower()

        ==

        invoice["vendor_name"]
        .strip()
        .lower()

    )

    invoice_number_match = (

        claim["invoice_number"]
        .strip()
        .upper()

        ==

        invoice["invoice_number"]
        .strip()
        .upper()

    )

    overall_match = (

        amount_match and
        vendor_match and
        invoice_number_match
    )

    return {

        "overall_match": overall_match,

        "amount_match": amount_match,

        "vendor_match": vendor_match,

        "invoice_number_match": invoice_number_match
    }