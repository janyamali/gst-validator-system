import re

from datetime import datetime


GSTIN_REGEX = r'[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}'


def normalize_ocr_text(text):

    replacements = {

        "■": "",

        "CG5T": "CGST",

        "5G5T": "SGST",

        "G5T1N": "GSTIN",

        "1nvoice": "Invoice",

        "Xeyboard": "Keyboard",

        "Put Lid": "Pvt Ltd",

        "cast": "CGST",

        "sast": "SGST",

        "m1350": "1350",

        "m350": "1350",

        "mas2": "2502",

        "m2s02": "2502",

        "12Z": "1Z5"
    }

    normalized = text

    for wrong, correct in replacements.items():

        normalized = normalized.replace(
            wrong,
            correct
        )

    return normalized


def extract_gstin(text):

    text = text.replace(
        " ",
        ""
    )

    pattern = r'[0-9]{2}[A-Z0-9]{13}'

    matches = re.findall(
        pattern,
        text
    )

    return matches[0] if matches else None


def extract_amount(pattern, text):

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        raw_value = match.group(1)

        cleaned = re.sub(
            r'[^0-9.]',
            '',
            raw_value
        )

        if not cleaned:
            return 0

        try:
            return float(cleaned)

        except:
            return 0

    return 0


def extract_vendor_name(text):

    match = re.search(
        r'Vendor[:\s]*(.*)',
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(1).strip()

    return "Unknown Vendor"


def extract_invoice_number(text):

    match = re.search(
        r'Invoice Number[:\s]*([A-Z0-9\-]+)',
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(1).strip()

    return "INV-TEMP"


def extract_invoice_date(text):

    patterns = [

        r'Invoice Date[:\s]*([\d]{4}-[\d]{2}-[\d]{2})',

        r'Invoice Date[:\s]*([\d]{2}/[\d]{2}/[\d]{4})',

        r'Date[:\s]*([\d]{4}-[\d]{2}-[\d]{2})',

        r'Date[:\s]*([\d]{2}/[\d]{2}/[\d]{4})'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    return str(
        datetime.today().date()
    )


def normalize_vendor_name(name: str):

    if not name:
        return None

    return name.strip().title()


def normalize_invoice_number(invoice_number: str):

    if not invoice_number:
        return None

    return invoice_number.strip().upper()


def parse_invoice_data(raw_invoice: dict):

    text = raw_invoice.get(
        "raw_text",
        ""
    )

    cleaned_text = normalize_ocr_text(text)

    print("\n========== RAW OCR TEXT ==========\n")

    print(text)

    print("\n========== CLEANED OCR TEXT ==========\n")

    print(cleaned_text)

    gstin = extract_gstin(
        cleaned_text
    )

    vendor_name = extract_vendor_name(
        cleaned_text
    )

    invoice_number = extract_invoice_number(
        cleaned_text
    )

    invoice_date = extract_invoice_date(
        cleaned_text
    )

    taxable_amount = extract_amount(
        r'Taxable\s*Amount[^0-9]*([0-9,]+)',
        cleaned_text
    )

    cgst = extract_amount(
        r'CGST[^0-9]*([0-9,]+)',
        cleaned_text
    )

    sgst = extract_amount(
        r'SGST[^0-9]*([0-9,]+)',
        cleaned_text
    )

    total_amount = extract_amount(
        r'Total\s*Amount[^0-9]*([0-9,]+)',
        cleaned_text
    )

    print("\n========== EXTRACTED VALUES ==========\n")

    print("Vendor Name:", vendor_name)

    print("GSTIN:", gstin)

    print("Invoice Number:", invoice_number)

    print("Invoice Date:", invoice_date)

    print("Taxable Amount:", taxable_amount)

    print("CGST:", cgst)

    print("SGST:", sgst)

    print("Total Amount:", total_amount)

    print("\n======================================\n")

    parsed_data = {

        "vendor_name": normalize_vendor_name(
            vendor_name
        ),

        "gstin": gstin,

        "invoice_number": normalize_invoice_number(
            invoice_number
        ),

        "invoice_date": invoice_date,

        "taxable_amount": taxable_amount,

        "cgst": cgst,

        "sgst": sgst,

        "igst": 0,

        "total_amount": total_amount
    }

    return parsed_data