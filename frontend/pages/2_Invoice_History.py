import streamlit as st
import pandas as pd

from services.api import get_invoices

st.title("📄 Invoice History")

data = get_invoices()

if isinstance(data, dict):

    st.error(
        data["error"]
    )

    st.stop()

if not data:

    st.warning(
        "No invoices found."
    )

    st.stop()

df = pd.DataFrame(data)

# =========================
# FILTERS
# =========================

st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:

    vendor_filter = st.text_input(
        "🔍 Search Vendor"
    )

with col2:

    gstin_filter = st.text_input(
        "🔍 Search GSTIN"
    )

col3, col4 = st.columns(2)

with col3:

    min_amount = st.number_input(
        "Minimum Amount",
        min_value=0.0,
        value=0.0
    )

with col4:

    max_amount = st.number_input(
        "Maximum Amount",
        min_value=0.0,
        value=float(df["total_amount"].max())
    )

# =========================
# APPLY FILTERS
# =========================

if vendor_filter:

    df = df[
        df["vendor_name"]
        .str.contains(
            vendor_filter,
            case=False,
            na=False
        )
    ]

if gstin_filter:

    df = df[
        df["gstin"]
        .str.contains(
            gstin_filter,
            case=False,
            na=False
        )
    ]

df = df[
    (df["total_amount"] >= min_amount)
    &
    (df["total_amount"] <= max_amount)
]

# =========================
# SUMMARY
# =========================

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Invoices Found",
    len(df)
)

col2.metric(
    "Total Amount",
    f"₹{df['total_amount'].sum():,.0f}"
)

col3.metric(
    "Unique Vendors",
    df["vendor_name"].nunique()
)

st.divider()

# =========================
# TABLE
# =========================

display_df = df[

    [

        "vendor_name",

        "gstin",

        "invoice_number",

        "invoice_date",

        "total_amount"

    ]

].copy()

display_df.columns = [

    "Vendor",

    "GSTIN",

    "Invoice Number",

    "Invoice Date",

    "Amount"

]

st.dataframe(

    display_df,

    use_container_width=True,

    hide_index=True
)