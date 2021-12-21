import numpy as np
import time
import mss.tools
import cv2
import sys
from helper_scripts import ocrify, process_text, search_sites, load_json, read_csv

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

    max_index = np.argmax(tot_wordrank)
    return(answers[max_index])

#SETUP
# question_source = ["CSV", "1WANS"] # ["OCR"] OR ["CSV", *question_number* OR "1WANS"]]
question_source = ["CSV", 22] # ["OCR"] OR ["CSV", *question_number* OR "1WANS"]]
ocr_type = "LOCAL" #LOCAL or ONLINE API
sites_ct = 7 #Range 1-7
tic = time.perf_counter()
filenames = setup()

#GET ROWS IF NEEDED
if (question_source[1] == "1WANS"):
    print("\nGetting 1WANS...")
    one_worders = read_csv.get_oneword()
    print("\t> Results: " + str(one_worders))
    sys.exit(0)

#GET TEXT
if (question_source[0] == "OCR"):
    question, answers = ocrify.run(ocr_type, filenames)
elif (question_source[0] == "CSV"):
    filter = question_source[1]
    if (type(filter) == int):
        question, answers = read_csv.local(question_source[1])
else:
    print("INVALID QUESTION SOURCE")

OCR_time = time.perf_counter()
print("\t> Done (" + str(round((OCR_time - tic), 2)) + " sec)")

#PROCESS TEXT
print("Processing text...")
question = process_text.process(question)
answers = process_text.process(answers)
print("\t> Processed Question: " + repr(question) + "")
print("\t> Processed Answers: " + repr(answers[0]) + ", " + repr(answers[1]) + ", " + repr(answers[2]))
Process_time = time.perf_counter()
print("\t> Done (" + str(round((Process_time - OCR_time), 2)) + " sec)")

#LOAD JSON
site_links = load_json.load(question)
JSON_time = time.perf_counter()
print("\t> Done (" + str(round((JSON_time - OCR_time), 2)) + " sec)")

#SEARCH EACH SITE
del site_links[sites_ct:]
pick = search(site_links, answers)
Search_time = time.perf_counter()
print("\t> Done (" + str(round((Search_time - JSON_time), 2)) + " sec)")

#CHECK ANSWER IF CSV USED
if (question_source[0] == "CSV"):
    print("Checking answer...")
    correct_ans = read_csv.get_correct_ans(question_source[1])
    print("\t> QUESTION: " + question)
    print("\t> PROGRAM ANS: " + pick)
    print("\t> CORRECT ANS: " + process_text.process(correct_ans))

Check_ans_time = time.perf_counter()
print("\t> Done (" + str(round((Check_ans_time - Search_time), 2)) + " sec)")

#END
toc = time.perf_counter()
print("\nFinished in " + str(round((toc-tic),2)) + " seconds")