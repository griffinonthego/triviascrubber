import time
import sys
from helper_scripts import ocrify, imaging, search_sites, load_json, read_csv, process_text, logging_tool

#SETUP (1WANS -> [3, 4, 5, 6, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
question_source = ["CSV", "ALL"] # ["OCR"] OR ["CSV", *question_number* OR "1WANS" OR "ALL"]]
ocr_type = "LOCAL" #LOCAL or ONLINE API
sites_ct = 0 #Range 1-7/8 or 0=max
tic_start = time.perf_counter()
filenames = imaging.take_images()
num_correct = 0

#GET ROWS IF NEEDED
if (question_source[1] == "1WANS"):
    question_source[1] = read_csv.get_oneword()

if (question_source[1] == "ALL"):
    question_source[1] = read_csv.get_all()

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
    # print("\t(" + str(round((OCR_time - tic), 2)) + " sec)")

    #PROCESS TEXT
    question = process_text.process(question)
    answers = process_text.process(answers)

    Process_time = time.perf_counter()
    # print("\t(" + str(round((Process_time - OCR_time), 2)) + " sec)")

    #LOAD JSON
    site_links = load_json.load(question)
    JSON_time = time.perf_counter()
    # print("\t(" + str(round((JSON_time - OCR_time), 2)) + " sec)")

    #SEARCH EACH SITE
    if (sites_ct > 0):
        del site_links[sites_ct:]

    search_sites.search_multi(site_links, answers, question_number)
    top_pick = answers[search_sites.get_max()]

    Search_time = time.perf_counter()
    # print("\t(" + str(round((Search_time - JSON_time), 2)) + " sec)")

    #CHECK ANSWER IF CSV USED
    if (question_source[0] == "CSV"):
        correct_ans = read_csv.get_correct_ans(question_number)
        correct_ans = process_text.process(correct_ans)

        if (correct_ans == top_pick):
            print(" > Correct", end = "")
        else:
            print(" > Incorrect", end = "")

        if (top_pick == process_text.process(correct_ans)):
            num_correct = num_correct + 1

    #END
    toc = time.perf_counter()
    print("\t(" + str(round((toc-tic),2)) + " sec)", end="\n")

final_toc = time.perf_counter()
total_time = str(round((final_toc-tic_start), 2))
logging_tool.save_run(total_time, num_correct, len(question_source[1]))