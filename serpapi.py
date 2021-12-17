import requests
import json
import time

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def do_search(search_term):
    serp_apikey = "e9a833d86a8647422dcbd09780978d45a25a67ebabed42d02a416ea18b5b981c"
    search_engine = "google"
    data = {"engine":search_engine, "apikey": serp_apikey, "q": search_term}

    method = "ONLINE"
    if (method == "JSON"):
        search_term = "test"
        data = json.load(open('google_test_json.json'))
        time.sleep(1)
    elif (method == "ONLINE"):
        response = requests.get("https://serpapi.com/search", data)
        data = response.json()

    print("Method: " + method  + " (\"" + search_term + "\")")
    site_links = [""] * 10
    ct = 0

    for i in data['organic_results']:
        site_links[ct] = i['link']
        ct = ct + 1
    return(site_links)

    # with open('trimmed_json.json','w') as outfile:
    #     json.dump(data, outfile, indent=4)
