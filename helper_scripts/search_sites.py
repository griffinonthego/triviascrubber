import requests
import numpy as np
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import time

import sys

def load_page(site):
    start_load = time.perf_counter()
    r = requests.get(site)
    soup = BeautifulSoup(r.content, features="html.parser")
    end_load = time.perf_counter()
    print("\t" + str(round((end_load - start_load), 2)) + " sec)", end ="")
    return soup

def do_search_wordrank(soup, answers):
    text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
    c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

    text_div = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
    c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))
    results = c_div + c_p

    totals = [results[answers[0]], results[answers[1]], results[answers[2]]]
    end_totals = time.perf_counter()

    return totals

def do_search_huntpeck(soup, answers):
    #Currently not working

    ct = 0
    totals = [0, 0, 0]
    for x in answers:
            if (soup.find(text = x) is not None):
                    totals[ct] = totals[ct] + 1
            ct = ct + 1
    return totals

def search(site_links, answers, q_num):
    site_links = [x for x in site_links if len(x) >= 3] #only get links that are more than a few characters long
    tot_huntpeck = [0, 0, 0]
    tot_wordrank = [0, 0, 0]
    ct = 0
    for site in site_links:
        soup = load_page(site)
        tot_huntpeck = np.add(tot_huntpeck, do_search_huntpeck(soup, answers))
        tot_wordrank = np.add(tot_wordrank, do_search_wordrank(soup, answers))
        max_index = np.argmax(tot_wordrank)

        sys.stdout.write("\rQ" + str(q_num) + " > Pick (%i): %s" % (ct+1, answers[max_index]))
        ct = ct + 1

    # print("\n\t> Search Method: HUNTPECK")
    # print("\t> Search Method: WORDRANK")
    ct = 0
    for i in answers:
        print("\n\t> " + str(i) + ": " + str(tot_huntpeck[ct]) + "," + str(tot_wordrank[ct]), end ="\t")
        ct = ct + 1
    print("\n")
    max_index = np.argmax(tot_wordrank)
    return(answers[max_index])


