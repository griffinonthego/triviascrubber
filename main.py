import numpy as np
import time
import sys
from helper_scripts import ocrify, imaging, search_sites, load_json, read_csv, process_text, logging

#SETUP (1WANS -> [3, 4, 5, 6, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
question_source = ["CSV", range(16, 18)] # ["OCR"] OR ["CSV", *question_number* OR "1WANS"]]
ocr_type = "LOCAL" #LOCAL or ONLINE API
sites_ct = 7 #Range 1-7
tic_start = time.perf_counter()
filenames = imaging.take_images()
num_correct = 0

#GET ROWS IF NEEDED
if (question_source[1] == "1WANS"):
    print("\nGetting 1WANS...")
    one_worders = read_csv.get_oneword()
    print("\t> Results: " + str(one_worders))
    sys.exit(0)

for question_number in question_source[1]:
    tic = time.perf_counter()
    #GET TEXT
    if (question_source[0] == "OCR"):
        question, answers = ocrify.run(ocr_type, filenames)
    elif (question_source[0] == "CSV"):
        question, answers = read_csv.local(question_number)
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
    top_pick = search_sites.search(site_links, answers)
    Search_time = time.perf_counter()
    print("\t> Done (" + str(round((Search_time - JSON_time), 2)) + " sec)")

    #CHECK ANSWER IF CSV USED
    if (question_source[0] == "CSV"):
        correct_ans = read_csv.get_correct_ans(question_number)
        correct_ans = process_text.process(correct_ans)
        print("> Summary... \n\t> " + top_pick + " vs. " + correct_ans)

        if (top_pick == process_text.process(correct_ans)):
            num_correct = num_correct + 1

    # Check_ans_time = time.perf_counter()
    # print("\t> Total time: " + str(round((Check_ans_time - Search_time), 2)) + " sec")

    #END
    toc = time.perf_counter()
    print("\t> Total Time: " + str(round((toc-tic),2)) + " sec")

final_toc = time.perf_counter()
total_time = str(round((final_toc-tic_start), 2))
logging.save_run(total_time, num_correct, len(question_source[1]))