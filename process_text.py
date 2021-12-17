def process(ocr_text):
    ocr_text = ocr_text.strip()
    ocr_text = ocr_text.replace("\n" ," ")
    ocr_text = ocr_text.replace("  ", " ")
    ocr_text = ocr_text.replace("\x0c", " ")
    ocr_text = ocr_text.lower()
    return ocr_text