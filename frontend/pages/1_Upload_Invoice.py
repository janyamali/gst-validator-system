import streamlit as st

from services.api import upload_invoice


st.title("📤 Upload Invoice")

employee_name = st.text_input(
    "Employee Name"
)

claim_number = st.text_input(
    "Claim Number"
)

claimed_amount = st.number_input(
    "Claim Amount",
    min_value=0.0
)

claimed_gst = st.number_input(
    "Claim GST",
    min_value=0.0
)

vendor_name = st.text_input(
    "Vendor Name"
)

invoice_number = st.text_input(
    "Invoice Number"
)

uploaded_file = st.file_uploader(
    "Choose PDF Invoice",
    type=["pdf"]
)

if st.button("Validate Invoice"):

    if uploaded_file:

        with st.spinner(
            "Processing Invoice..."
        ):

            result = upload_invoice(

                uploaded_file,

                employee_name,

                claim_number,

                claimed_amount,

                claimed_gst,

                vendor_name,

                invoice_number
            )

        if "error" in result:

            st.error(
                result["error"]
            )

        else:

            invoice = result["data"][0]["parsed_invoice"]

            validation = result["data"][0]["validation"]

            claim = result["data"][0]["claim_match"]

            duplicate = result["data"][0]["duplicate_detected"]

            st.success(
                "Invoice Processed Successfully"
            )

            st.subheader(
                "Invoice Information"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Vendor",
                    invoice["vendor_name"]
                )

                st.metric(
                    "GSTIN",
                    invoice["gstin"]
                )

            with col2:

                st.metric(
                    "Invoice Number",
                    invoice["invoice_number"]
                )

                st.metric(
                    "Total Amount",
                    f"₹{invoice['total_amount']}"
                )

            st.divider()

            st.subheader(
                "GST Validation"
            )

            if validation["overall_valid"]:

                st.success(
                    "GST Validation Passed"
                )

            else:

                st.error(
                    "GST Validation Failed"
                )

            st.write(
                f"GSTIN Valid: {'✅' if validation['gstin_valid'] else '❌'}"
            )

            st.write(
                f"GST Calculation Valid: {'✅' if validation['gst_valid'] else '❌'}"
            )

            st.write(
                f"Total Amount Valid: {'✅' if validation['total_valid'] else '❌'}"
            )

            st.write(
                f"Invoice Date Valid: {'✅' if validation['date_valid'] else '❌'}"
            )

            st.divider()

            st.subheader(
                "Claim Matching"
            )

            if claim["overall_match"]:

                st.success(
                    "Claim Matches Invoice"
                )

            else:

                st.error(
                    "Claim Mismatch Found"
                )

            st.write(
                f"Amount Match: {'✅' if claim['amount_match'] else '❌'}"
            )

            st.write(
                f"Vendor Match: {'✅' if claim['vendor_match'] else '❌'}"
            )

            st.write(
                f"Invoice Match: {'✅' if claim['invoice_number_match'] else '❌'}"
            )

            st.divider()

            if duplicate:

                st.warning(
                    "⚠ Duplicate Invoice Detected"
                )

            else:

                st.success(
                    "✅ No Duplicate Found"
                )

    else:

        st.error(
            "Please upload a PDF file."
        )