import streamlit as st

import pandas as pd

from services.api import (
    get_invoices
)

st.title(
    "📄 Invoice History"
)

data = get_invoices()

if isinstance(data, dict):

    st.error(
        data.get(
            "error",
            "Failed to load invoices."
        )
    )

else:

    df = pd.DataFrame(data)

    if df.empty:

        st.info("No invoices found.")

    else:

        st.dataframe(

            df[[
                "claim_voucher_number",
                "vendor_name",
                "invoice_number",
                "gstin",
                "taxable_amount",
                "cgst",
                "sgst",
                "igst",
                "total_amount",
                "claimed_amount",
                "claimed_gst",
                "validation_status"
            ]],

            use_container_width=True
        )