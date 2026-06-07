import streamlit as st

from services.api import (
    upload_invoice
)

st.title(
    "📄 GST Invoice Validation"
)

claims_excel = st.file_uploader(

    "Upload Claims Excel",

    type=["xlsx"]
)

invoice_pdf = st.file_uploader(

    "Upload Invoice PDF",

    type=["pdf"]
)

if st.button(
    "Validate Invoice"
):

    if not claims_excel:

        st.error(
            "Upload claims Excel."
        )

    elif not invoice_pdf:

        st.error(
            "Upload invoice PDF."
        )

    else:

        with st.spinner(
            "Validating..."
        ):

            result = upload_invoice(

                invoice_pdf,

                claims_excel
            )

        st.success(
            "Validation Complete"
        )

        st.json(result)