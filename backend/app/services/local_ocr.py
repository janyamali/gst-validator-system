import pytesseract

from PIL import Image

import fitz

import io



def extract_text_from_pdf(file_bytes):

    text = ""

    pdf_document = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    for page in pdf_document:

        pix = page.get_pixmap()

        img_bytes = pix.tobytes("png")

        image = Image.open(
            io.BytesIO(img_bytes)
        )

        page_text = pytesseract.image_to_string(image)

        text += page_text

    return text


def analyze_invoice(file_bytes):

    extracted_text = extract_text_from_pdf(
        file_bytes
    )

    return [
        {
            "raw_text": extracted_text
        }
    ]