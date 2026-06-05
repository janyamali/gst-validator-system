import streamlit as st
import pandas as pd
import plotly.express as px

from services.api import get_invoices

st.title("📈 Analytics")

data = get_invoices()

if isinstance(data, dict):

    st.error(
        data["error"]
    )

    st.stop()

if data:

    df = pd.DataFrame(data)

    fig = px.bar(

        df,

        x="vendor_name",

        y="total_amount",

        title="Invoice Value by Vendor"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "No invoice data available."
    )