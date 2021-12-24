import requests
import numpy as np
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import time
import threading

tot_huntpeck = [0, 0, 0]
tot_wordrank = [0, 0, 0]

def increment(add_huntpeck, add_wordrank):
    global tot_huntpeck
    global tot_wordrank

    tot_huntpeck = np.add(tot_huntpeck, add_huntpeck)
    tot_wordrank = np.add(tot_wordrank, add_wordrank)

def load_page(site):
    start_load = time.perf_counter()
    r = requests.get(site)
    soup = BeautifulSoup(r.content, features="html.parser")
    end_load = time.perf_counter()
    # print("\t(" + str(round((end_load - start_load), 2)) + " sec)", end ="")
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

def search(site, answers, lock):

    global tot_wordrank
    global tot_huntpeck

    soup = load_page(site)

    add_huntpeck = do_search_huntpeck(soup, answers)
    add_wordrank = do_search_wordrank(soup, answers)

    lock.acquire()
    increment(add_huntpeck, add_wordrank)
    lock.release()

    ct = 0
    for i in answers:
        # print("\n\t> " + str(i) + ": " + str(tot_huntpeck[ct]) + "," + str(tot_wordrank[ct]), end="\t")
        ct = ct + 1

def search_multi(site_links, answers):
    print("Running multi search", end=" >")

    lock = threading.Lock()

    t0 = threading.Thread(target=search, args=(site_links[0],answers,lock))
    t1 = threading.Thread(target=search, args=(site_links[1],answers,lock))
    t2 = threading.Thread(target=search, args=(site_links[2],answers,lock))
    t3 = threading.Thread(target=search, args=(site_links[3],answers,lock))
    t4 = threading.Thread(target=search, args=(site_links[4],answers,lock))
    t5 = threading.Thread(target=search, args=(site_links[5],answers,lock))

    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t0.join()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

start = time.perf_counter()
answers = ['blush','primer', 'cerulean']
site_links = ['https://quizlet.com/22064307/chapter-20-makeup-quiz-flash-cards/', 'https://www.makeupartistessentials.com/an-introduction-to-makeup-types-of-makeup/', 'https://en.wikipedia.org/wiki/Cosmetics', 'https://revolutioninkgallery.com/lgojnd/what-is-pigment-used-for-in-makeup.html', 'https://www.medicalnewstoday.com/articles/327318', 'https://books.google.com/books?id=hcEKAAAAQBAJ&pg=PT606&lpg=PT606&dq=which+of+these+is+both+a+color+and+a+common+kind+of+makeup?&source=bl&ots=NPdbQlY3eP&sig=ACfU3U28db_jnbunl-jVOy1vzv0JWoxkbA&hl=en&sa=X&ved=2ahUKEwjx8tzb2PP0AhWHVN8KHSWMDDwQ6AF6BAglEAM', 'https://books.google.com/books?id=jmYPEAAAQBAJ&pg=PA85&lpg=PA85&dq=which+of+these+is+both+a+color+and+a+common+kind+of+makeup?&source=bl&ots=xM9lSzZqXn&sig=ACfU3U27nfgSNIdMyv_enxO7V_2pKS4iyg&hl=en&sa=X&ved=2ahUKEwjx8tzb2PP0AhWHVN8KHSWMDDwQ6AF6BAgjEAM']
search_multi(site_links, answers)
end = time.perf_counter()

print("\n(" + str(round((end - start), 2)) + " sec)", end ="")
