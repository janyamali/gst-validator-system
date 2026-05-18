# def analyze_invoice(file_bytes):

#     return [
#         {
#             "vendor_name": "   reliance retail ltd   ",

#             "gstin": "27abcde1234f1z5",

#             "invoice_number": " inv-1001 ",

#             "invoice_date": "2026-05-16",

#             "taxable_amount": "1000",

#             "cgst": "90",

#             "sgst": "90",

#             "igst": "0",

#             "total_amount": "1180"
#         }


# Dulicate false 

# def analyze_invoice(file_bytes):

#     return [
#         {
#             "vendor_name": "Tata Electronics Pvt Ltd",

#             "gstin": "29PQRSX5678L1Z2",

#             "invoice_number": "INV-2002",

#             "invoice_date": "2026-05-16",

#             "taxable_amount": "5000",

#             "cgst": "450",

#             "sgst": "450",

#             "igst": "0",

#             "total_amount": "5900"
#         }
#     ]

# INVALID 
def analyze_invoice(file_bytes):

    return [
        {
            "vendor_name": "Fake Electronics Pvt Ltd",

            "gstin": "29AAAAA1111A1Z1",

            "invoice_number": "INV-9999",

            "invoice_date": "2026-05-16",

            "taxable_amount": "5000",

            "cgst": "50",

            "sgst": "50",

            "igst": "0",

            "total_amount": "7000"
        }
    ]