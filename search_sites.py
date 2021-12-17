import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation

def do_search(site_links):
    print("\t" + site_links[0])
    r = requests.get(site_links[0])
    soup = BeautifulSoup(r.content, features="html.parser")

    text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
    c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

    text_div = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
    c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))

    total = c_div + c_p
    print(len(total))

site_links = ['']*10
site_links[0] = 'https://en.wikipedia.org/wiki/Never_Gonna_Give_You_Up'
do_search(site_links)

