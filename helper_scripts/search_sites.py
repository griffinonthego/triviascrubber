import requests
import numpy as np
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import sys

def do_search_wordrank(site, answers):
        r = requests.get(site)
        soup = BeautifulSoup(r.content, features="html.parser")

        text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
        c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

        text_div = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
        c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))
        results = c_div + c_p

        totals = [results[answers[0]], results[answers[1]], results[answers[2]]]
        return totals

def do_search_huntpeck(site, answers):
        #Currently not working
        r = requests.get(site)
        soup = BeautifulSoup(r.content, features="html.parser")

        ct = 0
        totals = [0, 0, 0]
        for x in answers:
                if (soup.find(text = x) is not None):
                        totals[ct] = totals[ct] + 1
                ct = ct + 1
        return totals

def search(site_links, answers):
    print("Searching Sites... \n\t> ", end = "")
    tot_huntpeck = [0, 0, 0]
    tot_wordrank = [0, 0, 0]
    ct = 0
    for site in site_links:
        tot_huntpeck = np.add(tot_huntpeck, do_search_huntpeck(site, answers))
        tot_wordrank = np.add(tot_wordrank, do_search_wordrank(site, answers))
        # print(str(ct), end = " ")
        # # sys.stdout.flush()
        max_index = np.argmax(tot_wordrank)

        sys.stdout.write("\r\t> Live Pick (%i): %s" % (ct+1, answers[max_index]))
        ct = ct + 1

    print("\n\t> Search Method: HUNTPECK")
    print("\t> Search Method: WORDRANK")
    ct = 0
    for i in answers:
        print("\t\t> " + str(i) + ": \t" + str(tot_huntpeck[ct]) + "\t" + str(tot_wordrank[ct]))
        ct = ct + 1

    max_index = np.argmax(tot_wordrank)
    return(answers[max_index])

