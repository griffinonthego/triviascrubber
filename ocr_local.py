import pytesseract
from PIL import Image
import string

def ocrify(q_image):
    ocr_text = pytesseract.image_to_string(Image.open(q_image));

    return ocr_text