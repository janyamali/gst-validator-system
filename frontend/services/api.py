import requests

import os

BASE_URL = os.getenv(
    "BACKEND_URL",
    "https://gst-validator-system.onrender.com"
)


def get_invoices():

    try:

        response = requests.get(
            f"{BASE_URL}/invoices/",
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:

        return {
            "error": "Server timeout. Render may be waking up."
        }

    except requests.exceptions.ConnectionError:

        return {
            "error": "Unable to connect to server."
        }

    except Exception as e:

        return {
            "error": str(e)
        }


def export_excel():

    return f"{BASE_URL}/export/excel"


def upload_invoice(
    file,
    employee_name,
    claim_number,
    claimed_amount,
    claimed_gst,
    vendor_name,
    invoice_number
):

    try:

        files = {
            "file": file
        }

        data = {

            "employee_name": employee_name,

            "claim_number": claim_number,

            "claimed_amount": claimed_amount,

            "claimed_gst": claimed_gst,

            "vendor_name": vendor_name,

            "invoice_number": invoice_number
        }

        response = requests.post(

            f"{BASE_URL}/upload/",

            files=files,

            data=data,

            timeout=60
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:

        return {
            "error": "OCR processing timeout."
        }

    except requests.exceptions.ConnectionError:

        return {
            "error": "Cannot connect to backend."
        }

    except Exception as e:

        return {
            "error": str(e)
        }