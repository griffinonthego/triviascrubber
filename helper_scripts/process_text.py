
def modify_text(ocr_text):
    ocr_text = ocr_text.strip()
    ocr_text = ocr_text.replace("\n", " ")
    ocr_text = ocr_text.replace("  ", " ")
    ocr_text = ocr_text.replace("\x0c", " ")
    ocr_text = ocr_text.lower()
    return ocr_text

def process(text):
    if (isinstance(text, str)):
        text = modify_text(text)
        # print("\t> Processed Question: " + text + "")
        return text
    elif (isinstance(text, list)):
        ct = 0
        answers = [""] * len(text)
        for i in text:
            answers[ct] = modify_text(i)
            ct = ct + 1
        # print("\t> Processed Text: " + str(answers) + "")
        return answers

def link_to_foldername(site):

