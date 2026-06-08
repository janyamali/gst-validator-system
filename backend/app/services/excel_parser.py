import pandas as pd
from io import BytesIO


def load_claims_excel(excel_content):

    import pandas as pd
    from io import BytesIO

    df = pd.read_excel(
        BytesIO(excel_content)
    )

    print("\nEXCEL COLUMNS:")
    print(df.columns.tolist())

    return df


def find_claim_by_invoice_number(
    invoice_number,
    claims_df
):

    claims_df.columns = (
        claims_df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    invoice_number = (
    str(invoice_number)
    .strip()
    .replace("-", "")
    .replace(" ", "")
    .upper()
    )

    match = claims_df[

    claims_df["invoice_number"]

    .astype(str)

    .str.strip()

    .str.replace("-", "", regex=False)

    .str.replace(" ", "", regex=False)

    .str.upper()

    ==

    invoice_number
    ]

    if len(match) == 0:

        return None

    return match.iloc[0].to_dict()