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

import re

def extract_cgst(text):

    patterns = [

        r'CGST.*?([\d,]+\.\d+)',

        r'CGST\s*\(?[\d.]*%?\)?\s*([\d,]+\.\d+)',

        r'Central\s+Tax.*?([\d,]+\.\d+)'

    ]

    for pattern in patterns:

        match = re.search(

            pattern,

            text,

            re.IGNORECASE | re.DOTALL

        )

        if match:

            return float(

                match.group(1).replace(",", "")

            )

    return 0

import re

def extract_sgst(text):

    patterns = [

        r'SGST.*?([\d,]+\.\d+)',

        r'SGST\s*\(?[\d.]*%?\)?\s*([\d,]+\.\d+)',

        r'State\s+Tax.*?([\d,]+\.\d+)'

    ]

    for pattern in patterns:

        match = re.search(

            pattern,

            text,

            re.IGNORECASE | re.DOTALL

        )

        if match:

            return float(

                match.group(1).replace(",", "")

            )

    return 0

import re

def extract_total_amount(text):

    patterns = [

        r'Gross\s+Amount/?Total\s*[:\-]?\s*₹?\s*([\d,]+\.\d+)',

        r'Total\s+Amount\s*[:\-]?\s*₹?\s*([\d,]+\.\d+)',

        r'Invoice\s+Value\s*[:\-]?\s*₹?\s*([\d,]+\.\d+)',

        r'Grand\s+Total\s*[:\-]?\s*₹?\s*([\d,]+\.\d+)'

    ]

    for pattern in patterns:

        match = re.search(

            pattern,

            text,

            re.IGNORECASE

        )

        if match:

            return float(

                match.group(1).replace(",", "")

            )

    # Fallback

    matches = re.findall(

        r'[\d,]+\.\d+',

        text

    )

    if matches:

        return max(

            float(x.replace(",", ""))

            for x in matches

        )

    return 0

import re


def extract_taxable_amount(text):

    patterns = [

        r"Total\s+Taxable\s+Value\s*[:\-]?\s*₹?\s*([\d,]+\.\d+)",

        r"Taxable\s+Amount\s*[:\-]?\s*₹?\s*([\d,]+\.\d+)",

        r"Sub\s*Total\s*[:\-]?\s*₹?\s*([\d,]+\.\d+)",

        r"Net\s*Amount\s*[:\-]?\s*₹?\s*([\d,]+\.\d+)"

    ]

    for pattern in patterns:

        match = re.search(

            pattern,

            text,

            re.IGNORECASE

        )

        if match:

            amount = match.group(1)

            amount = amount.replace(",", "")

            return float(amount)

    # -----------------------------
    # Fallback
    # -----------------------------

    matches = re.findall(

        r'[\d,]+\.\d+',

        text

    )

    candidates = []

    for value in matches:

        num = float(

            value.replace(",", "")

        )

        if num >= 100:

            candidates.append(num)

    if candidates:

        return min(candidates)

    return 0


import re

def extract_vendor_name(text):

    lines = text.splitlines()

    for i, line in enumerate(lines):

        if "Sold By" in line:

            if i + 1 < len(lines):

                return lines[i + 1].strip().upper()

        if "Supplier Information" in line:

            for j in range(i + 1, min(i + 8, len(lines))):

                candidate = lines[j].strip()

                if len(candidate) > 5:

                    return candidate.upper()

    blacklist = [

        "",

        "tax invoice",

        "invoice",

        "original for recipient",

        "billing address",

        "shipping address",

        "customer details",

        "supplier information",

        "recipient information",

        "delivery information",

        "legal name",

        "trade name",

        "document no",

        "document date",

        "gstin",

        "gst registration",

        "state",

        "place of supply"

    ]

    # First preference:
    # company immediately before GSTIN

    for i, line in enumerate(lines):

        if "GSTIN" in line.upper() or "GST REGISTRATION" in line.upper():

            for j in range(i - 1, max(i - 6, -1), -1):

                candidate = lines[j].strip()

                if len(candidate) < 3:
                    continue

                if any(word in candidate.lower() for word in blacklist):
                    continue

                if re.search(r"\d{2}[A-Z]{5}\d{4}", candidate):
                    continue

                return candidate.upper()

    # Second preference:
    # first company-like name

    for line in lines:

        candidate = line.strip()

        if len(candidate) < 5:
            continue

        if any(word in candidate.lower() for word in blacklist):
            continue

        if any(

            keyword in candidate.upper()

            for keyword in [

                "LTD",

                "LIMITED",

                "LLP",

                "PVT",

                "PRIVATE",

                "ENTERPRISE",

                "CONSULTANTS",

                "ASSOCIATES"

            ]

        ):

            return candidate.upper()

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


import re
from datetime import datetime


def extract_invoice_date(text):

    patterns = [

        r'Invoice\s*Date\s*[:\-]?\s*(\d{1,2}[./-][A-Za-z]{3}[./-]\d{2,4})',

        r'Invoice\s*Date\s*[:\-]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})',

        r'Document\s*Date\s*[:\-]?\s*(\d{1,2}[./-][A-Za-z]{3}[./-]\d{2,4})',

        r'Document\s*Date\s*[:\-]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})',

        r'Dated\s*[:\-]?\s*(\d{1,2}[./-][A-Za-z]{3}[./-]\d{2,4})',

        r'Dated\s*[:\-]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})'
    ]

    for pattern in patterns:

        match = re.search(

            pattern,

            text,

            re.IGNORECASE

        )

        if match:

            date_str = match.group(1).strip()

            formats = [

                "%d-%b-%Y",

                "%d-%b-%y",

                "%d.%m.%Y",

                "%d.%m.%y",

                "%d/%m/%Y",

                "%d/%m/%y",

                "%Y-%m-%d"

            ]

            for fmt in formats:

                try:

                    return datetime.strptime(

                        date_str,

                        fmt

                    ).strftime("%Y-%m-%d")

                except:

                    pass

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

def extract_invoice_block(text, invoice_number):

    if invoice_number == "INV-TEMP":
        return text

    start = text.find(invoice_number)

    if start == -1:
        return text

    previous_markers = [
        "Sold By",
        "Tax Invoice",
        "Invoice",
        "ORIGINAL FOR RECIPIENT",
        "Customer Details"
    ]

    previous = -1

    for marker in previous_markers:

        pos = text.rfind(marker, 0, start)

        if pos > previous:
            previous = pos

    if previous == -1:
        previous = max(0, start - 600)

    next_markers = [
        "Page 2",
        "Page 3",
        "Sold By",
        "Tax Invoice"
    ]

    next_pos = len(text)

    for marker in next_markers:

        pos = text.find(marker, start + len(invoice_number))

        if pos != -1 and pos < next_pos:
            next_pos = pos

    return text[previous:next_pos]


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

    print("\n========== INVOICE BLOCK ==========")
    print(f"Invoice Block Length: {len(invoice_block)}")
    print(invoice_block[:700])
    print("==================================")

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

    