import gc
import io

import cv2
import fitz
import numpy as np
import pytesseract
from PIL import Image


def preprocess_image(image):

    image_np = np.array(image)

    gray = cv2.cvtColor(
        image_np,
        cv2.COLOR_BGR2GRAY
    )

    threshold = cv2.threshold(
        gray,
        150,
        255,
        cv2.THRESH_BINARY
    )[1]

    return threshold


def extract_text_from_pdf(file_bytes):

    text = ""

    pdf_document = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    for page in pdf_document:

        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        img_bytes = pix.tobytes("png")

        image = Image.open(
            io.BytesIO(img_bytes)
        )

        processed_image = preprocess_image(
            image
        )

        page_text = pytesseract.image_to_string(
            processed_image,
            config="--psm 6"
        )

        text += page_text + "\n"

        # Free memory immediately
        del pix
        del img_bytes
        del image
        del processed_image

        gc.collect()

    pdf_document.close()

    return text


def analyze_invoice(file_bytes):

    extracted_text = extract_text_from_pdf(
        file_bytes
    )

    print("\n========== OCR SUMMARY ==========")
    print(f"Characters extracted: {len(extracted_text)}")
    print("\nPreview:\n")
    print(extracted_text[:500])
    print("\n=================================")

    return {
        "raw_text": extracted_text
    }