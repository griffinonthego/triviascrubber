import requests
import json

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def fixtext(text):
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("  ", " ")
    return text

def ocrify(q_image):
    api_key = "12739a035188957"
    data = {"apikey": api_key}
    file = {'file': open('saved_ref.png', 'rb')}

    response = requests.post("https://api.ocr.space/parse/image",data,files=file)
    data = response.json()
    # COMMENT THIS LINE vv AND UNCOMMED THAT LINE ^^ FOR ONLINE USE
    # data = json.load(open('test_json.json'))

    # jprint(data)

    ocr_text = str(data['ParsedResults'][0]['ParsedText'])
    ocr_text = fixtext(ocr_text)
    return ocr_text




