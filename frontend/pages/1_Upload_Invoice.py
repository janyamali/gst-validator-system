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

invoice_pdfs = st.file_uploader(
    "Upload Invoice PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if invoice_pdfs:

    st.write(
        f"Selected {len(invoice_pdfs)} PDFs"
    )

    for pdf in invoice_pdfs:

        st.write(
            "📄",
            pdf.name
        )

if st.button(
    "Validate Invoice"
):

    if not claims_excel:

        st.error(
            "Upload claims Excel."
        )

    elif not invoice_pdfs:

        st.error(
            "Upload at least one invoice PDF."
        )

    else:

        with st.spinner(
            "Validating..."
        ):

            result = upload_invoice(
                invoice_pdfs,
                claims_excel
            )

        st.success(
            "Validation Complete"
        )

        if not result.get("success"):

            st.error(
                "Validation failed."
            )

        else:

            for item in result["data"]:

                st.divider()

                # Handle invoice not found
                if "error" in item:

                    st.error(
                        item["error"]
                    )

                    continue

                status = item.get(
                    "status",
                    "UNKNOWN"
                )

                if status == "VALID":

                    st.success(
                        f"✅ Status: {status}"
                    )

                else:

                    st.error(
                        f"❌ Status: {status}"
                    )

                parsed_invoice = item.get(
                    "parsed_invoice",
                    {}
                )

                claim_data = item.get(
                    "claim_data",
                    {}
                )

                validation = item.get(
                    "validation",
                    {}
                )

                claim_match = item.get(
                    "claim_match",
                    {}
                )

                st.subheader(
                    "Invoice Details"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "**Vendor:**",
                        parsed_invoice.get(
                            "vendor_name"
                        )
                    )

                    st.write(
                        "**Invoice Number:**",
                        parsed_invoice.get(
                            "invoice_number"
                        )
                    )

                    st.write(
                        "**GSTIN:**",
                        parsed_invoice.get(
                            "gstin"
                        )
                    )

                with col2:

                    st.write(
                        "**Invoice Date:**",
                        parsed_invoice.get(
                            "invoice_date"
                        )
                    )

                    st.write(
                        "**Total Amount:** ₹",
                        parsed_invoice.get(
                            "total_amount"
                        )
                    )

                    st.write(
                        "**Claim Amount:** ₹",
                        claim_data.get(
                            "claimed_amount"
                        )
                    )

                st.subheader(
                    "Validation Results"
                )

                st.write(
                    "GST Valid:",
                    validation.get(
                        "gst_valid"
                    )
                )

                st.write(
                    "Total Valid:",
                    validation.get(
                        "total_valid"
                    )
                )

                st.write(
                    "Date Valid:",
                    validation.get(
                        "date_valid"
                    )
                )

                st.write(
                    "Duplicate Invoice:",
                    item.get(
                        "duplicate_detected"
                    )
                )

                st.subheader(
                    "Claim Matching"
                )

                st.write(
                    "Invoice Match:",
                    claim_match.get(
                        "invoice_number_match"
                    )
                )

                st.write(
                    "Vendor Match:",
                    claim_match.get(
                        "vendor_match"
                    )
                )

                st.write(
                    "Amount Match:",
                    claim_match.get(
                        "amount_match"
                    )
                )

                st.write(
                    "GST Match:",
                    claim_match.get(
                        "gst_match"
                    )
                )

                st.subheader(
                    "🤖 AI Audit Explanation"
                )

                ai_reason = item.get(
                    "ai_reason",
                    "No AI explanation available."
                )

                with st.expander(
                    "View AI Explanation",
                    expanded=True
                ):

                    st.write(
                        ai_reason
                    )

                st.subheader(
                    "Raw Response"
                )

                st.json(
                    item
                )