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

    gstin_pattern = r"\b\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[A-Z0-9]\b"

    match = re.search(

        gstin_pattern,

        text,

        re.IGNORECASE

    )

    if match:

        gstin = match.group()

        gstin = gstin.upper()

        return gstin

    return None

def extract_numeric_value_from_line(keyword, text):

    if keyword == "CGST":

        match = re.search(
            r'CGST\|?\s*(\d+\.\d+)',
            text,
            re.IGNORECASE
        )

        if match:

            return float(
                match.group(1)
            )

    elif keyword == "SGST":

        match = re.search(
            r'SGST\|?\s*(\d+\.\d+)',
            text,
            re.IGNORECASE
        )

        if match:

            return float(
                match.group(1)
            )

    return 0

def extract_taxable_amount(text):

    matches = re.findall(
        r'(\d+\.\d+)',
        text
    )

    candidates = []

    for value in matches:

        num = float(value)

        if 100 <= num <= 10000:

            candidates.append(num)

    if candidates:

        return min(candidates)

    return 0


def calculate_taxable_from_items(text):

    lines = text.splitlines()

    for line in lines:

        if "EWC" in line or "NOS" in line:

            numbers = re.findall(
                r'\d+',
                line
            )

            if numbers:

                try:

                    return int(
                        numbers[-1]
                    )

                except:
                    pass

    return 0


def extract_vendor_name(text):

    patterns = [

        r"Sold By\s*:?\s*(.+)",

        r"Supplier\s*:?\s*(.+)",

        r"Supplier Name\s*:?\s*(.+)",

        r"Vendor\s*:?\s*(.+)",

        r"Legal Name\s*:?\s*(.+)",

        r"Issued By\s*:?\s*(.+)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            vendor = match.group(1)

            vendor = vendor.split("\n")[0]

            vendor = vendor.strip()

            if len(vendor) > 3:

                return vendor

    return "Unknown Vendor"

import re

def extract_invoice_number(text):

    patterns = [

        r'Invoice\s*Number\s*[:\-]?\s*([A-Z0-9\/\-]+)',
        r'Invoice\s*No\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)',
        r'Invoice\s*#\s*[:\-]?\s*([A-Z0-9\/\-]+)',

        r'Tax\s*Invoice\s*No\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)',

        r'Document\s*No\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)',
        r'Document\s*Number\s*[:\-]?\s*([A-Z0-9\/\-]+)',

        r'Doc\s*No\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)',

        r'Bill\s*No\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)',

        r'Reference\s*No\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)',

        r'Ref\s*No\.?\s*[:\-]?\s*([A-Z0-9\/\-]+)',

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            invoice = match.group(1)

            invoice = invoice.strip()

            invoice = invoice.replace(" ", "")

            return invoice

    return "INV-TEMP"

def extract_claim_voucher_number(text):

    patterns = [

        r'Claim Voucher Number[:\s]*([A-Z0-9\-]+)',

        r'Claim Voucher No[:\s]*([A-Z0-9\-]+)',

        r'Voucher Number[:\s]*([A-Z0-9\-]+)',

        r'Voucher No[:\s]*([A-Z0-9\-]+)'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return None


def extract_invoice_date(text):

    patterns = [

        r'Invoice\s*Date\s*[:\-]?\s*(\d{2}[./-]\d{2}[./-]\d{4})',

        r'Document\s*Date\s*[:\-]?\s*(\d{2}[./-]\d{2}[./-]\d{4})',

        r'Bill\s*Date\s*[:\-]?\s*(\d{2}[./-]\d{2}[./-]\d{4})',

        r'(\d{2}[./-]\d{2}[./-]\d{4})',

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            date = match.group(1)

            date = date.replace(".", "-")

            date = date.replace("/", "-")

            day, month, year = date.split("-")

            return f"{year}-{month}-{day}"

    return None

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

def extract_invoice_block(
    text,
    invoice_number
):

    if invoice_number == "INV-TEMP":

        return text

    start = text.find(invoice_number)

    if start == -1:

        return text

    previous = text.rfind(
        "Sold By",
        0,
        start
    )

    if previous == -1:

        previous = max(
            0,
            start - 400
        )

    next_invoice = text.find(
        "Sold By",
        start + len(invoice_number)
    )

    if next_invoice == -1:

        next_invoice = len(text)

    block = text[
        previous:next_invoice
    ]

    return block

def extract_cgst(text):

    match = re.search(
        r'CGST\|\s*(\d+\.\d+)',
        text,
        re.IGNORECASE
    )

    if match:

        value = float(
            match.group(1)
        )

        if value > 20:

            value = round(
                value / 6,
                2
            )

        return value

    return 0

def extract_sgst(text):

    match = re.search(
        r'SGST\|\s*(\d+\.\d+)',
        text,
        re.IGNORECASE
    )

    if match:

        value = float(
            match.group(1)
        )

        if value > 20:

            value = round(
                value / 6,
                2
            )

        return value

    return 0

def extract_total_amount(text):

    amounts = re.findall(
        r'(\d+\.\d+)',
        text
    )

    amounts = [

        float(x)

        for x in amounts

        if float(x) > 200
    ]

    if amounts:

        return max(amounts)

    return 0

def parse_invoice_data(raw_invoice: dict):

    text = raw_invoice.get(
        "raw_text",
        ""
    )

    cleaned_text = normalize_ocr_text(
        text
    )


    print(f"Raw OCR Length: {len(text)}")
    print(text[:500])

    
    print(f"Cleaned OCR Length: {len(cleaned_text)}")
    print(cleaned_text[:500])

    invoice_number = extract_invoice_number(
        cleaned_text
    )

    print(
        "\nINVOICE NUMBER FOUND:",
        invoice_number
    )

    invoice_block = extract_invoice_block(
        cleaned_text,
        invoice_number
    )

    print(
        "\n========== INVOICE BLOCK ==========\n",
        len(invoice_block)
    )

    print(f"Invoice Block Length: {len(invoice_block)}")
    print(invoice_block[:700])

    vendor_name = extract_vendor_name(
        invoice_block
    )

    gstin = extract_gstin(
        invoice_block
    )

    claim_voucher_number = extract_claim_voucher_number(
        invoice_block
    )

    print(
        "Claim Voucher Number:",
        claim_voucher_number
    )

    invoice_date = extract_invoice_date(
        invoice_block
    )

    taxable_amount = extract_taxable_amount(
        invoice_block
    )

    cgst = extract_cgst(
        invoice_block
    )

    sgst = extract_sgst(
        invoice_block
    )

    total_amount = extract_total_amount(
        invoice_block
    )

    print("\nBEFORE AUTO CORRECT")
    print("Taxable:", taxable_amount)
    print("CGST:", cgst)
    print("SGST:", sgst)
    print("Total:", total_amount)

    if taxable_amount == 0 and total_amount > 0:

        taxable_amount = round(
            total_amount / 1.18
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

    confidence = 0

    if vendor_name and vendor_name != "Unknown Vendor":
        confidence += 25

    if gstin:
        confidence += 25

    if invoice_number and invoice_number != "INV-TEMP":
        confidence += 25

    if total_amount > 0 and taxable_amount > 0:
        confidence += 25

    if cgst > 0 and sgst > 0:
        confidence += 25

    confidence = min(
    confidence,
    100
    )

    print(
        f"\nPARSER CONFIDENCE: {confidence}%"
    )

    return {

        "vendor_name": normalize_vendor_name(
            vendor_name
        ),

        "gstin": gstin,

        "invoice_number": normalize_invoice_number(
            invoice_number
        ),

        "claim_voucher_number": claim_voucher_number,

        "invoice_date": invoice_date,

        "taxable_amount": taxable_amount,

        "cgst": cgst,

        "sgst": sgst,

        "igst": 0,

        "total_amount": total_amount,

        "confidence": confidence
    }

    