from paddleocr import PaddleOCR

import fitz

import numpy as np

from PIL import Image

import io


ocr = PaddleOCR(
    use_angle_cls=False,
    lang='en',
    show_log=False,
    use_gpu=False
)


def pdf_to_images(file_bytes):

    images = []

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

        image_np = np.array(image)

        images.append(image_np)

    return images


def analyze_invoice(file_bytes):

    images = pdf_to_images(file_bytes)

    full_text = ""

    for image in images:

        result = ocr.ocr(
            image,
            cls=False
        )

        for line in result[0]:

            text = line[1][0]

            full_text += text + " "

    print("\nPADDLE OCR TEXT:\n")

    print(full_text)

    return [
        {
            "raw_text": full_text
        }
    ]