import numpy as np
import time
import mss.tools
import cv2
import sys
from helper_scripts import ocrify, process_text, search_sites, serpapi


def printarray(array):
    for i in array:
        print(i)
def setup():
    q_bb = {'top': 230, 'left': 30, 'width': 300, 'height': 175}
    a1_bb = {'top': 450, 'left': 80, 'width': 200, 'height': 50}
    a2_bb = {'top': 520, 'left': 80, 'width': 200, 'height': 50}
    a3_bb = {'top': 590, 'left': 80, 'width': 200, 'height': 50}

    sct = mss.mss()
    pdir = 'app_images/'
    filenames = {
        'question_image':pdir+'q.png',
        'processed_question_image':pdir+'pq.png',
        'answer_image':pdir+'a.png',
        'processed_answer_image':pdir+'a.png',
        'answer1_image':pdir+'a1.png',
        'answer2_image':pdir+'a2.png',
        'answer3_image':pdir+'a3.png',
    }

    # Arrange Window Locaitions
    cv2.namedWindow("Question")
    cv2.moveWindow("Question", 360, 0)
    cv2.namedWindow("a1")
    cv2.moveWindow("a1", 360, 380)
    cv2.namedWindow("a2")
    cv2.moveWindow("a2", 360, 510)
    cv2.namedWindow("a3")
    cv2.moveWindow("a3", 360, 640)

    # Get question, Display and save it
    q = sct.grab(q_bb)
    a1 = sct.grab(a1_bb)
    a2 = sct.grab(a2_bb)
    a3 = sct.grab(a3_bb)

    cv2.imshow('Question', np.array(q))
    cv2.imshow('a1', np.array(a1))
    cv2.imshow('a2', np.array(a2))
    cv2.imshow('a3', np.array(a3))

    mss.tools.to_png(q.rgb, q.size, output=filenames['question_image'])
    mss.tools.to_png(a1.rgb, a1.size, output=filenames['answer1_image'])
    mss.tools.to_png(a2.rgb, a2.size, output=filenames['answer2_image'])
    mss.tools.to_png(a3.rgb, a3.size, output=filenames['answer3_image'])
    return filenames
def run_ocr(method,filenames):
    print("\nPerfoming OCR...\n\t> Processing Method: " + method)
    if method == "ONLINE API":
        question = ocrify.online(filenames['question_image'])
        answer1 = ocrify.online(filenames['answer1_image'])
        answer2 = ocrify.online(filenames['answer2_image'])
        answer3 = ocrify.online(filenames['answer3_image'])
    elif method == "LOCAL":
        question = ocrify.local(filenames['question_image'])
        answer1 = ocrify.local(filenames['answer1_image'])
        answer2 = ocrify.local(filenames['answer2_image'])
        answer3 = ocrify.local(filenames['answer3_image'])
    else:
        print("\t> INVALID SEARCH METHOD")
        sys.exit(1)
    answers = [answer1, answer2, answer3]

    return question, answers
def run_processing(text):
    if (isinstance(text, str)):
        text = process_text.process(text)
        return text
    elif (isinstance(text, list)):
        ct = 0
        for i in text:
            answers[ct] = process_text.process(i)
            ct = ct + 1
        return text
def run_googling(method, question):
    print("Perfoming Google Search...")
    site_links = serpapi.do_search(method, question)
    while ('' in site_links):
        site_links.remove('')
    print("\t> Links Result: " + str(site_links))
    return site_links
def search(site_links, answers):
    print("Searching Sites...")
    tot_huntpeck = [0, 0, 0]
    tot_wordrank = [0, 0, 0]
    for site in site_links:
    # search_sites.do_search_huntpeck(site_links[0], answers)
        tot_huntpeck = np.add(tot_huntpeck, search_sites.do_search_huntpeck(site, answers))
        tot_wordrank = np.add(tot_wordrank, search_sites.do_search_wordrank(site, answers))

    print("\t> Search Method: HUNTPECK")
    print("\t> Search Method: WORDRANK")
    ct = 0
    for i in answers:
        print("\t\t> " + str(i) + ": \t" + str(tot_huntpeck[ct]) + "\t" + str(tot_wordrank[ct]))
        ct = ct + 1

#Start Timer
tic = time.perf_counter()

#General Setup
filenames = setup()

#Run OCR
question, answers = run_ocr("LOCAL", filenames) #LOCAL or ONLINE API

#Further Process Text
question = run_processing(question)
answers = run_processing(answers)

print("\t> Question Result: " + repr(question) + "")
print("\t> Answers Result: " + repr(answers[0]) + ", " + repr(answers[1]) + ", " + repr(answers[2]))
OCR_time = time.perf_counter()
print("\t> Done (" + str(OCR_time-tic) + " sec)")

#Google the Question
site_links = run_googling("ONLINE API",question) #TEST JSON or ONLINE API
Google_time = time.perf_counter()
print("\t> Done (" + str(Google_time - OCR_time) + " sec)")

#Search the Sites
search(site_links, answers)
Search_time = time.perf_counter()
print("\t> Done (" + str(Search_time - Google_time) + " sec)")

# End timer
toc = time.perf_counter()
print("\nFinished in " + str(toc-tic) + "seconds")
