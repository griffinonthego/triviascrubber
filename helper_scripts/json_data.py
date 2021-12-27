import requests
import json
import time
import sys
from os.path import exists
from helper_scripts import read_csv, process_text

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def load(question):
    serp_apikey = "e9a833d86a8647422dcbd09780978d45a25a67ebabed42d02a416ea18b5b981c"
    search_engine = "google"

    data = {"engine":search_engine, "apikey": serp_apikey, "q": question}
    csv_number = read_csv.get_question_number(question)
    json_path = 'json_files/' + str(csv_number + 1) + '.json'
    json_exists = exists(json_path)

    if (json_exists == False):
        print("\t> JSON not found, performing new search...", end = "")

        response = requests.get("https://serpapi.com/search", data)
        data = response.json()
        save_json(data, json_path)
    else:
        # print("> JSON found locally...", end ="")
        data = json.load(open(json_path))

    try:
        site_links = get_links(data)
    except:
        site_links = []

    return site_links
#
def save_json(data, json_path):
    outfile =  open(json_path, 'w')
    json.dump(data, outfile, indent=4)

def get_links(data):
    site_links = [""] * 10
    ct = 0

    for i in data['organic_results']:
        site_links[ct] = i['link']
        ct = ct + 1

    return site_links

