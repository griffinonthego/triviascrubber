import requests
import json
import time
import sys
from os.path import exists
import logging
from helper_scripts import read_csv, process_text
indent = '    '


def print(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def local_load(question_number):
    logger = logging.getLogger(__name__)

    json_path = 'archives/json/' + str(question_number) + '.json'
    json_exists = exists(json_path)

    if(json_exists):
        logger.info(indent*2 + "Local JSON found...")
        data = json.load(open(json_path))
        site_links = get_links(data)
        for link in site_links:
            logger.info(indent*3 + str(link)[0:40])
    else:
        logger.error("json_data.remote_load() not finished")
        quit()

    if (site_links == []):
        logger.error("JSON load failed")
        quit()

    return site_links

# def remote_load(question_number):
    # serp_apikey = "e9a833d86a8647422dcbd09780978d45a25a67ebabed42d02a416ea18b5b981c"
    # search_engine = "google"
    #
    # data = {"engine": search_engine, "apikey": serp_apikey, "q": question}
    # json_path = 'archives/json/' + str(question_number + 1) + '.json'
    # json_exists = exists(json_path)
    #
    # print("\t> JSON not found, performing new search...", end="")
    #
    # response = requests.get("https://serpapi.com/search", data)
    # data = response.json()
    # save_json(data, json_path)
    #
    # try:
    #     site_links = get_links(data)
    # except:
    #     site_links = []


def save(data, json_path):
    outfile =  open(json_path, 'w')
    json.dump(data, outfile, indent=4)

def get_links(data):
    site_links = [""] * 10
    ct = 0

    for i in data['organic_results']:
        site_links[ct] = i['link']
        ct = ct + 1

    return site_links

