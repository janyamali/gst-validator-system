import requests

import os

BASE_URL = os.getenv(
    "BACKEND_URL",
    "https://gst-validator-backend.onrender.com"
)   


def get_invoices():

    try:

        response = requests.get(
            f"{BASE_URL}/invoices/"
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }


def export_excel():

    return f"{BASE_URL}/export/excel"


def upload_invoice(
    invoice_pdfs,
    claims_excel
):

    try:

        files = []

        for pdf in invoice_pdfs:

            files.append(

                (
                    "invoice_pdfs",
                    (
                        pdf.name,
                        pdf.getvalue(),
                        "application/pdf"
                    )
                )
            )

        files.append(

            (
                "claims_excel",
                (
                    claims_excel.name,
                    claims_excel.getvalue(),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            )
        )

        response = requests.post(

            f"{BASE_URL}/upload/",

            files=files,

            timeout=300
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }