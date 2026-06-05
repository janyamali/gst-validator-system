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

if data:

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No invoices found."
    )