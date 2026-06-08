def match_claim_with_invoice(
    claim,
    invoice
):

    voucher_match = (

        str(
            claim["claim_voucher_number"]
        ).strip().upper()

        ==

        str(
            invoice["claim_voucher_number"]
        ).strip().upper()
    )

    amount_match = (

        abs(
            float(
                claim["claimed_amount"]
            )

            -

            float(
                invoice["total_amount"]
            )

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

    gst_match = (

        abs(

            float(
                claim["claimed_gst"]
            )

            -

            (

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

        ) <= 2
    )

    overall_match = (

        amount_match

        and

        vendor_match

        and

        invoice_number_match

        and

        gst_match
    )

    return {

        "overall_match":
        overall_match,

        "voucher_match":
        voucher_match,

        "amount_match":
        amount_match,


        "invoice_number_match":
        invoice_number_match,

        "gst_match":
        gst_match
    }