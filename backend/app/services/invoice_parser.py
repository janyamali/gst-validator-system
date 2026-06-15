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

    lines = text.splitlines()

    keyword_aliases = {

        "CGST": ["CGST", "C GST"],

        "SGST": ["SGST", "S GST"],

        "TOTAL": [
            "Total Amount",
            "Grand Total",
            "Nettotal"
        ]
    }

    search_terms = keyword_aliases.get(
        keyword,
        [keyword]
    )

    for line in lines:

        if any(

            term.lower() in line.lower()

            for term in search_terms
        ):

            print(
                f"\nMATCHED LINE FOR {keyword}: {line}"
            )

            numbers = re.findall(
                r'\d+',
                line
            )

            print(
                f"NUMBERS FOUND: {numbers}"
            )

            if numbers:

                return float(
                    numbers[-1]
                )

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

    # AMAZON / MARKETPLACE
    sold_by_match = re.search(
        r"Sold By\s*:?\s*\n?\s*([A-Z0-9 &.,()\-]+)",
        text,
        re.IGNORECASE
    )

    if sold_by_match:

        vendor = sold_by_match.group(1).strip()

        if vendor:

            return vendor

    # SWIGGY

    restaurant_match = re.search(
        r"Restaurant Name\s*:?\s*([^\n]+)",
        text,
        re.IGNORECASE
    )

    if restaurant_match:

        vendor = restaurant_match.group(1).strip()

        if vendor:

            return vendor

    # STANDARD INVOICE

    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()
    ]

    for line in lines:

        if "invoice no" in line.lower():

            vendor = re.split(
                r'Invoice\s+No',
                line,
                flags=re.IGNORECASE
            )[0].strip()

            if vendor:

                return vendor

    # FIRST NON-EMPTY LINE FALLBACK

    blacklist = [

        "tax invoice",
        "invoice",
        "bill of supply",
        "cash memo",
        "subject to",
        "gstin"
    ]

    for line in lines:

        if not any(

            bad in line.lower()

            for bad in blacklist
        ):

            if len(line) > 3:

                return line

    return "Unknown Vendor"


def extract_invoice_number(text):

    patterns = [

        r'Invoice\s+No[:\s]*([A-Z0-9\-]+)',

        r'Invoice\s+No\.?[:\s]*([A-Z0-9\-]+)',

        r'Invoice\s+Number[:\s]*([A-Z0-9\-]+)',

        r'Invoice\s*#[:\s]*([A-Z0-9\-]+)'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return (
                match.group(1)
                .strip()
                .upper()
            )

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

        r'(\d{2}-\d{2}-\d{4})',

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

                elif len(date_str) == 10 and date_str[2] == "-":

                    return datetime.strptime(
                        date_str,
                        "%d-%m-%Y"
                    ).strftime("%Y-%m-%d")

                return date_str

            except:
                pass

    return str(datetime.today().date())

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

    cleaned_text = normalize_ocr_text(
        text
    )

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

    claim_voucher_number = extract_claim_voucher_number(
        cleaned_text
    )

    print(
        "Claim Voucher Number:",
        claim_voucher_number
    )

    invoice_date = extract_invoice_date(
        cleaned_text
    )

    taxable_amount = calculate_taxable_from_items(
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
        "TOTAL",
        cleaned_text
    )

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

        "total_amount": total_amount
    }