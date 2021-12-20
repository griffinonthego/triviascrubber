

apikey = 'AIzaSyDMV20oPq9Y-GR7cFc4Ey5s5qrhJN9Onwg'
cse_id = 'griffinsoule.tk'

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res