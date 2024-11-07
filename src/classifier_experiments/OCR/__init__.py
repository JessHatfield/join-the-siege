import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, 500)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text

# Usage
image_path = 'driving_licenses/drivers_license_1.jpg'
extracted_text = extract_text_from_image(image_path)
print(extracted_text)

# Usage
pdf_path = 'bank_statements/bank_statement_2.pdf'
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)