import pytesseract
from PIL import Image

def ocrify(q_image):
    ocr_text = pytesseract.image_to_string(Image.open(q_image));
    ocr_text = ocr_text.replace("\n"," ")
    ocr_text = ocr_text.replace("  ", " ")
    return ocr_text