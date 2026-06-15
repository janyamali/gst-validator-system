import pandas as pd
from io import BytesIO


def load_claims_excel(excel_content):

    df = pd.read_excel(
        BytesIO(excel_content)
    )

    df.columns = (

        df.columns

        .str.strip()

        .str.lower()

        .str.replace(" ", "_")
    )

    print("\nEXCEL COLUMNS:")
    print(df.columns.tolist())

    return df


def find_claim_by_invoice_number(
    invoice_number,
    claims_df
):

    invoice_number = (
        str(invoice_number)
        .strip()
        .replace("-", "")
        .replace(" ", "")
        .upper()
    )

    print("\nEXCEL COLUMNS:")
    print(claims_df.columns.tolist())

    print("\nLOOKING FOR:")
    print(invoice_number)

    # ---------------------------------
    # Find invoice column automatically
    # ---------------------------------

    possible_columns = [

        "invoice_number",

        "invoice_no",

        "bill_number",

        "claim_voucher_no",

        "voucher_no"
    ]

    search_column = None

    for col in possible_columns:

        if col in claims_df.columns:

            search_column = col

            break

    if search_column is None:

        raise Exception(
            f"No invoice column found. Available columns: {claims_df.columns.tolist()}"
        )

    print(f"\nUSING COLUMN: {search_column}")

    match = claims_df[

        claims_df[search_column]

        .astype(str)

        .str.strip()

        .str.replace("-", "", regex=False)

        .str.replace(" ", "", regex=False)

        .str.upper()

        ==

        invoice_number
    ]

    if len(match) == 0:

        print("\nNO MATCH FOUND")

        return None

    claim = match.iloc[0].to_dict()

    return normalize_claim(
        claim
    )


def normalize_claim(claim):

    normalized = {}

    normalized["invoice_number"] = (

        claim.get("invoice_number")

        or

        claim.get("invoice_no")

        or

        claim.get("bill_number")

        or

        claim.get("claim_voucher_no")

        or

        claim.get("voucher_no")
    )

    normalized["vendor_name"] = (

        claim.get("vendor")

        or

        claim.get("vendor_name")

        or

        claim.get("supplier")

        or

        ""
    )

    normalized["claimed_amount"] = (

        claim.get("total")

        or

        claim.get("amount")

        or

        claim.get("claimed_amount")

        or

        0
    )

    normalized["claimed_gst"] = (

        float(
            claim.get("cgst", 0)
        )

        +

        float(
            claim.get("sgst", 0)
        )

        +

        float(
            claim.get("igst", 0)
        )
    )

    normalized["raw_data"] = claim

    print("\nNORMALIZED CLAIM DATA:")
    print(normalized)

    return normalized