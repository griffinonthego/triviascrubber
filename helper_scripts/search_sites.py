import bs4
import requests
import numpy as np
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import time
import sys
import threading
import os.path
from os import path
from hashlib import sha256

tot_huntpeck = [0, 0, 0]
tot_wordrank = [0, 0, 0]
link_num = 0
failures = 0
sites_dir = 'archives/websites/'

def increment(add_huntpeck, add_wordrank):
    global tot_huntpeck
    global tot_wordrank
    tot_huntpeck = np.add(tot_huntpeck, add_huntpeck)
    tot_wordrank = np.add(tot_wordrank, add_wordrank)

def update_console(answers, q_num):
    global link_num
    global failures
    link_num = link_num + 1
    sys.stdout.write("\rQ" + str(q_num) + " > Pick (%i): %s (%i failures)" % (link_num, answers[get_max()], failures))

def get_max():
    max_index = np.argmax(tot_wordrank)
    return max_index

def save_site(site, q_num, soup):
    print("\t> Saving site...")
    p = sites_dir + str(q_num) + "/"
    hash = sha256(site.encode()).hexdigest()[:13]
    filename = f'{hash}.html'
    # filename = p + filename
    print(filename)
    with open(filename, 'w+') as f:
        f.write(str(soup))
    # print(os.getxattr(filename, 'user.url').decode())
    print("done")


def site_exists(site, q_num):
    print("Checking if folder for Q" + str(q_num) + " exists...")
    
    if (path.exists(sites_dir + str(q_num)) is not True):
        print("Directory not found, creatig path")
        os.mkdir(sites_dir + str(q_num))
    elif (path.exists(sites_dir + str(q_num)) is True):
        print("Directory found, reading")

    print("Checking if link in Q" + str(q_num) + " exists...")

    if (path.exists(sites_dir + str(q_num) + "/" + site) is not True):
        return -1
    elif (path.exists(sites_dir + str(q_num) + "/" + site) is True):
        p = sites_dir + str(q_num) + "/" + site
        return p


def load_page(site, q_num):
    p = site_exists(site, q_num)
    if (p != -1):
        print("\t> Local webarchive found, reading...")
        # try:
        #
        # except:
        #     soup = 0
    elif (p == -1):
        print("\t> Local webarchive NOT found, loading...")
        try:
            r = requests.get(site)
            soup = BeautifulSoup(r.content, features="html.parser")
            save_site(site, q_num,soup)
        except:
            soup = 0
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
    ct = 0
    totals = [0, 0, 0]
    for x in answers:
            if (soup.find(text = x) is not None):
                    totals[ct] = totals[ct] + 1
            ct = ct + 1
    return totals

def clear_globals():
    global tot_wordrank
    global tot_huntpeck
    global link_num
    global failures
    tot_huntpeck = [0, 0, 0]
    tot_wordrank = [0, 0, 0]
    link_num = 0
    failures = 0

def filter_bad_sites(site_links):
    site_links = [x for x in site_links if len(x) >= 3] #Removes links with less than 3 characters
    return site_links

def show_tallies(answers):
    ct = 0
    for i in answers:
        print("\n\t\t> " + str(i) + ": " + str(tot_huntpeck[ct]) + "," + str(tot_wordrank[ct]), end="\t")
        ct = ct + 1
    print("\n")

def run(site, answers, q_num, lock):
    global tot_wordrank
    global tot_huntpeck
    global link_num
    global failures

    soup = load_page(site, q_num)

    if (type(soup) == bs4.BeautifulSoup):
        add_huntpeck = do_search_huntpeck(soup, answers)
        add_wordrank = do_search_wordrank(soup, answers)
        lock.acquire()
        increment(add_huntpeck, add_wordrank)
        lock.release()
    if (type(soup) == int):
        failures = failures + 1

    update_console(answers, q_num)
    # show_tallies(answers)

def search_multi(site_links, answers, q_num):
    clear_globals()
    site_links = filter_bad_sites(site_links)

    lock = threading.Lock()
    threads = []

    for x in range(len(site_links)):
        t = threading.Thread(target=run, args=(site_links[x],answers,q_num,lock))
        t.start()
        threads.append(t)

    for x in threads:
        x.join()

def search_lin(site_links, answers, q_num):
    clear_globals()
    global tot_wordrank
    global tot_huntpeck
    global failures
    site_links = filter_bad_sites(site_links)

    for site in site_links:
        soup = load_page(site, q_num)
        if (type(soup) == bs4.BeautifulSoup):
            increment(do_search_huntpeck(soup, answers), do_search_wordrank(soup, answers),)
        elif(type(soup) == int):
            failures = failures + 1

        update_console(answers, q_num)

    # show_tallies(answers)
