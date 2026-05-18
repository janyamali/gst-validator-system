import pytesseract

import fitz

from PIL import Image

import io

import cv2

import numpy as np


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

    enlarged = cv2.resize(
        threshold,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    return enlarged


def extract_text_from_pdf(file_bytes):

    text = ""

    pdf_document = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    for page in pdf_document:

        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))

        img_bytes = pix.tobytes("png")

        image = Image.open(
            io.BytesIO(img_bytes)
        )

        processed_image = preprocess_image(
            image
        )

        page_text = pytesseract.image_to_string(
            processed_image,
            config='--psm 6'
        )

        text += page_text + "\n"

    return text


def analyze_invoice(file_bytes):

    extracted_text = extract_text_from_pdf(
        file_bytes
    )

    print("\n========== OCR TEXT ==========\n")

    print(extracted_text)

    return [
        {
            "raw_text": extracted_text
        }
    ]