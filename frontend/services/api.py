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
    invoice_pdf,
    claims_excel
):

    try:

        files = {

            "invoice_pdf": (

                invoice_pdf.name,

                invoice_pdf,

                "application/pdf"
            ),

            "claims_excel": (

                claims_excel.name,

                claims_excel,

                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        }

        response = requests.post(

            f"{BASE_URL}/upload/",

            files=files,

            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }