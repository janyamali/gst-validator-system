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

    seller_patterns = [

        r"GST Registration No[:\s]*([0-9A-Z]{15})",

        r"Seller GSTIN[:\s]*([0-9A-Z]{15})",

        r"GSTIN[:\s]*([0-9A-Z]{15})"
    ]

    for pattern in seller_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(1)

    matches = re.findall(
        r'[0-9]{2}[A-Z0-9]{13}',
        text
    )

    return matches[0] if matches else None


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

    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()
    ]

    # AMAZON STYLE
    # Sold By:
    # MIRADH ENTERPRISES

    for i, line in enumerate(lines):

        if "sold by" in line.lower():

            if i + 1 < len(lines):

                vendor = lines[i + 1].strip()

                if len(vendor) > 2:

                    return vendor

    # AMAZON STYLE
    # For ICC CHEMTEC PVT LTD

    for line in lines:

        if line.lower().startswith("for "):

            vendor = (

                line.replace("For", "")
                .replace(":", "")
                .strip()
            )

            if len(vendor) > 3:

                return vendor

    # EXISTING STYLE
    # Synergy Electronics Invoice No ...

    for line in lines:

        if "invoice no" in line.lower():

            vendor = re.split(
                r'Invoice\s+No',
                line,
                flags=re.IGNORECASE
            )[0].strip()

            if vendor:

                return vendor

    blacklist = [

        "tax invoice",
        "billing address",
        "shipping address",
        "invoice",
        "invoice details",
        "invoice to"
    ]

    for line in lines[:10]:

        if line.lower() not in blacklist:

            if len(line) > 4:

                return line

    return "Unknown Vendor"


def extract_invoice_number(text):

    matches = re.findall(

        r'Invoice\s*Number\s*[:]\s*([A-Z0-9\-]+)',

        text,

        re.IGNORECASE
    )

    if matches:

        # Ignore Amazon marketplace invoices

        filtered = [

            m.upper()

            for m in matches

            if not m.upper().startswith("MKT")
        ]

        if filtered:

            return filtered[-1]

        return matches[-1].upper()

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

        r'(\d{2}/\d{2}/\d{4})',

        r'(\d{2}\.\d{2}\.\d{4})',

        r'(\d{4}-\d{2}-\d{2})'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            date_str = match.group(1)

            try:

                if "/" in date_str:

                    return datetime.strptime(
                        date_str,
                        "%d/%m/%Y"
                    ).strftime("%Y-%m-%d")

                elif "." in date_str:

                    return datetime.strptime(
                        date_str,
                        "%d.%m.%Y"
                    ).strftime("%Y-%m-%d")

                else:

                    return date_str

            except Exception as e:

                print(
                    "DATE PARSE ERROR:",
                    e
                )

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

def extract_invoice_block(
    text,
    invoice_number
):

    sections = text.split(
        "Sold By"
    )

    for section in sections:

        if invoice_number in section:

            return section

    return text

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

    print("\n========== RAW OCR TEXT ==========\n")
    print(text)

    print("\n========== CLEANED OCR TEXT ==========\n")
    print(cleaned_text)

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

    print(invoice_block)

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

    