import requests
import json
import time
import pytesseract
import PIL.Image
import sys
import process_text
import read_csv

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def fixtext(text):
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("  ", " ")
    return text

def read_images_to_csv():
    number_range = range(2875,2898)
    for image_number in number_range:
        pdir = 'app_images/'
        filenames = {
            'question_image': pdir + 'q.png',
            'processed_question_image': pdir + 'pq.png',
            'answer_image': pdir + 'a.png',
            'processed_answer_image': pdir + 'a.png',
            'answer1_image': pdir + 'a1.png',
            'answer2_image': pdir + 'a2.png',
            'answer3_image': pdir + 'a3.png',
        }

        print("Running read_from_files OCR")
        dir = 'test_images/additional_questions/uncropped/'
        img_start_num = str(image_number)
        img_prefix = "IMG_"
        img_suffix = ".PNG"
        filename = dir + img_prefix + img_start_num + img_suffix
        print(filename)
        image = PIL.Image.open(filename)
        question = image.crop((120, 475, 1050, 1325))
        a1 = image.crop((180, 1450, 980, 1640))
        a2 = image.crop((180, 1690, 980, 1880))
        a3 = image.crop((180, 1930, 980, 2120))

        question.save(filenames['question_image'], format="png")
        a1.save(filenames['answer1_image'], format="png")
        a2.save(filenames['answer2_image'], format="png")
        a3.save(filenames['answer3_image'], format="png")

        # image.show()
        # question.show()
        # a1.show()
        # a2.show()
        # a3.show()

        question, answers = run("ONLINE API", filenames)
        print(question)
        print(answers)
        read_csv.add_q_and_as(question, answers)

def crop_raw():
    print("Cropping...")

def online(image):
    ocr_apikey = "12739a035188957"
    data = {"apikey": ocr_apikey}
    file = {'file': open(image, 'rb')}

    method = "IMAGE"
    print("\t> Source: " + method)
    if (method == "JSON"):
        data = json.load(open('../json_files/test_json.json'))
        time.sleep(1)
    elif (method == "IMAGE"):
        print("\t\t> Sending POST Request...")
        response = requests.post("https://api.ocr.space/parse/image",data,files=file)
        data = response.json()
        print("\t\t> Response: " + str(response.status_code))
        if (response.status_code == 403):
            print("\t> Request declined by server > ", end = "")
            jprint(data)
            sys.exit()

    ocr_text = str(data['ParsedResults'][0]['ParsedText'])
    ocr_text = fixtext(ocr_text)
    return ocr_text

def local(image):
    ocr_text = pytesseract.image_to_string(PIL.Image.open(image));
    return ocr_text

def run(ocr_type, filenames):
    print("\nPerfoming OCR... \n\t> Processing Method: " + ocr_type)
    if ocr_type == "ONLINE API":
        question = online(filenames['question_image'])
        answer1 = online(filenames['answer1_image'])
        answer2 = online(filenames['answer2_image'])
        answer3 = online(filenames['answer3_image'])
    elif ocr_type == "LOCAL":
        question = local(filenames['question_image'])
        answer1 = local(filenames['answer1_image'])
        answer2 = local(filenames['answer2_image'])
        answer3 = local(filenames['answer3_image'])
    else:
        print("\t> INVALID SEARCH METHOD")
        sys.exit(0)
    answers = [answer1, answer2, answer3]
    return question, answers
