import logging
indent = '    '

def modify_text(ocr_text):
    ocr_text = ocr_text.strip()
    ocr_text = ocr_text.replace("\n", " ")
    ocr_text = ocr_text.replace("  ", " ")
    ocr_text = ocr_text.replace("\x0c", " ")
    ocr_text = ocr_text.lower()
    return ocr_text

def process(text):
    logger = logging.getLogger(__name__)

    if (isinstance(text, str)):
        text = modify_text(text)
        logger.info(2*indent + "Q: " + text)
        return text
    elif (isinstance(text, list)):
        ct = 0
        answers = [""] * len(text)
        for i in text:
            answers[ct] = modify_text(i)
            ct = ct + 1
        logger.info(2*indent + "A: " + str(answers))
        return answers

