def match_claim_with_invoice(
    claim,
    invoice
):

    invoice_number_match = (

        str(
            claim["invoice_number"]
        ).strip().upper()

        ==

        str(
            invoice["invoice_number"]
        ).strip().upper()
    )

    amount_match = (

        abs(

            float(
                claim["total"]
            )

            -

            float(
                invoice["total_amount"]
            )

        ) <= 2
    )

    vendor_match = (

        str(
            claim["vendor"]
        ).strip().lower()

        in

        str(
            invoice["vendor_name"]
        ).strip().lower()
    )

    claimed_gst = (

        float(
            claim["cgst"]
        )

        +

        float(
            claim["sgst"]
        )
    )

    invoice_gst = (

        float(
            invoice["cgst"]
        )

        +

        float(
            invoice["sgst"]
        )

        +

        float(
            invoice["igst"]
        )
    )

    gst_match = (

        abs(
            claimed_gst
            -
            invoice_gst
        ) <= 2
    )

    overall_match = (

        invoice_number_match

        and

        amount_match

        and

        gst_match
    )

    return {

        "overall_match":
        overall_match,

        "invoice_number_match":
        invoice_number_match,

        "amount_match":
        amount_match,

        "vendor_match":
        vendor_match,

        "gst_match":
        gst_match
    }
