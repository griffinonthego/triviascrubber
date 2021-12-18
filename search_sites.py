import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation

def do_search(site, answers):
        r = requests.get(site)
        soup = BeautifulSoup(r.content, features="html.parser")

        # text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
        # c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))
        #
        # text_div = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
        # c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))
        # results = c_div + c_p
        #
        # totals = [results[answers[0]], results[answers[1]], results[answers[2]]]
        # return totals

        results = soup.find_all(text=lambda text: text and 'the' in text)
        print(results)


