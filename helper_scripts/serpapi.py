import requests
import json
import time
import sys

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def do_search(method, search_term):
    serp_apikey = "e9a833d86a8647422dcbd09780978d45a25a67ebabed42d02a416ea18b5b981c"
    search_engine = "google"
    data = {"engine":search_engine, "apikey": serp_apikey, "q": search_term}

    print("\t> Response Source: " + method)
    if (method == "TEST JSON"):
        search_term = "the music of rick astley played a direct role in bringing down the leader of what country?"
        data = json.load(open('json_files/google_test_json.json'))
        time.sleep(1)
    elif (method == "ONLINE API"):
        response = requests.get("https://serpapi.com/search", data)
        data = response.json()

        with open('json_files/saved_json.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
    else:
        print("\t> INVALID SEARCH METHOD")
        sys.exit(1)

    site_links = [""] * 10
    ct = 0

    for i in data['organic_results']:
        site_links[ct] = i['link']
        ct = ct + 1

    return(site_links)


