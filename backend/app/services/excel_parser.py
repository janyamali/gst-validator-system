import pandas as pd
from io import BytesIO


def load_claims_excel(excel_bytes):

    df = pd.read_excel(
        BytesIO(excel_bytes)
    )

    df.columns = [
        col.strip().lower()
        for col in df.columns
    ]

    return df


def find_claim_by_voucher(
    voucher_number,
    claims_df
):

    matches = claims_df[

        claims_df[
            "claim_voucher_number"
        ].astype(str).str.strip()

        ==

        str(voucher_number).strip()
    ]

    if len(matches) == 0:

        return None

    row = matches.iloc[0]

    return {

        "claim_voucher_number":
        row["claim_voucher_number"],

        "employee_name":
        row["employee_name"],

        "vendor_name":
        row["vendor_name"],

        "invoice_number":
        row["invoice_number"],

        "claimed_amount":
        float(row["claimed_amount"]),

        "claimed_gst":
        float(row["claimed_gst"])
    }