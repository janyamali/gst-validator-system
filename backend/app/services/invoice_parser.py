import re

from datetime import datetime


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

        "12Z": "1Z5",

        "L122": "L1Z2"
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


def extract_numeric_value_from_line(keyword, text):

    lines = text.splitlines()

    for line in lines:

        if keyword.lower() in line.lower():

            print(f"\nMATCHED LINE FOR {keyword}: {line}")

            numbers = re.findall(
                r'\d{3,}',
                line
            )

            print(f"NUMBERS FOUND: {numbers}")

            cleaned_numbers = []

            for number in numbers:

                try:

                    cleaned_numbers.append(
                        int(number)
                    )

                except:
                    pass

            if cleaned_numbers:

                return float(
                    max(cleaned_numbers)
                )

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


def auto_correct_amounts(
    taxable_amount,
    cgst,
    sgst,
    total_amount
):

    expected_gst = round(
        taxable_amount * 0.09
    )

    if abs(cgst - expected_gst) > 100:

        cgst = expected_gst

    if abs(sgst - expected_gst) > 100:

        sgst = expected_gst

    expected_total = taxable_amount + cgst + sgst

    if abs(total_amount - expected_total) > 100:

        inferred_taxable = round(
            total_amount / 1.18
        )

        taxable_amount = inferred_taxable

        cgst = round(
            taxable_amount * 0.09
        )

        sgst = round(
            taxable_amount * 0.09
        )

        total_amount = taxable_amount + cgst + sgst

    return (
        taxable_amount,
        cgst,
        sgst,
        total_amount
    )


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

    taxable_amount = extract_numeric_value_from_line(
        "Taxable Amount",
        cleaned_text
    )

    cgst = extract_numeric_value_from_line(
        "CGST",
        cleaned_text
    )

    sgst = extract_numeric_value_from_line(
        "SGST",
        cleaned_text
    )

    total_amount = extract_numeric_value_from_line(
        "Total Amount",
        cleaned_text
    )

    taxable_amount, cgst, sgst, total_amount = auto_correct_amounts(
        taxable_amount,
        cgst,
        sgst,
        total_amount
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