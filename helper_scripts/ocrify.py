import requests
import json
import time
import pytesseract
import PIL.Image

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def fixtext(text):
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("  ", " ")
    return text

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

    # jprint(data)

    ocr_text = str(data['ParsedResults'][0]['ParsedText'])
    ocr_text = fixtext(ocr_text)
    return ocr_text

def local(image):
    ocr_text = pytesseract.image_to_string(PIL.Image.open(image));
    return ocr_text




