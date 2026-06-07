import streamlit as st

import pandas as pd

from services.api import (
    get_invoices
)

st.title(
    "📈 Analytics"
)

data = get_invoices()

if isinstance(data, dict):

    st.error(
        data.get(
            "error",
            "Failed to load data."
        )
    )

else:

    df = pd.DataFrame(data)

    total = len(df)

    valid = len(

        df[
            df[
                "validation_status"
            ]
            ==
            "VALID"
        ]
    )

    invalid = total - valid

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Invoices",
        total
    )

    c2.metric(
        "Valid",
        valid
    )

    c3.metric(
        "Invalid",
        invalid
    )

    st.bar_chart(

        df[
            "validation_status"
        ].value_counts()
    )