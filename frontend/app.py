import streamlit as st
import pandas as pd
from services.api import get_invoices

st.set_page_config(
    page_title="GST Validator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 GST Validator Dashboard")

try:

    invoices = get_invoices()

    total_invoices = len(invoices)

    total_gst = sum(
        i["cgst"] + i["sgst"] + i["igst"]
        for i in invoices
    )

    total_value = sum(
        i["total_amount"]
        for i in invoices
    )

    unique_vendors = len(
        set(
            i["vendor_name"]
            for i in invoices
        )
    )

except:

    total_invoices = 0
    total_gst = 0
    total_value = 0
    unique_vendors = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Invoices",
    total_invoices
)

col2.metric(
    "GST Collected",
    f"₹{total_gst:,.0f}"
)

col3.metric(
    "Invoice Value",
    f"₹{total_value:,.0f}"
)

col4.metric(
    "Vendors",
    unique_vendors
)

st.divider()

st.info(
    "Use the sidebar to upload invoices, analyze data, and export reports."
)