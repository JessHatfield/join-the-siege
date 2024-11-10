import io

import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
from werkzeug.datastructures import FileStorage

from src.enums.document_types import SupportedFileTypes


def extract_text_from_image(file: FileStorage) -> str:
    image_bytes = file.read()
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text


def extract_text_from_pdf(file: FileStorage):
    image_bytes = file.read()
    pages = convert_from_bytes(image_bytes)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text


def extract_text_from_file(file, file_type):

    if file_type == SupportedFileTypes.PDF.value:
        text = extract_text_from_pdf(file)

    elif file_type == SupportedFileTypes.JPG.value or file_type == SupportedFileTypes.PNG.value:
        text = extract_text_from_image(file)

    else:
        raise ValueError(f'Could Not Identify Extraction Function For File With MimeType Of {file_type}')

    return text
