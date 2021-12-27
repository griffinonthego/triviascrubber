import time
import sys
from helper_scripts import ocrify, imaging, search_sites, json_data, read_csv, process_text, logging_tool

#SETUP (1WANS -> [3, 4, 5, 6, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
question_source = ["CSV", "ALL"] # ["OCR"] OR ["CSV", *question_number* OR "1WANS" OR "ALL"]]
ocr_source = "LOCAL"
ocr_type = "ONLINE API" #LOCAL or ONLINE API
search_type = "MULTI" #MULTI = Multithreaded, LIN = Linear
sites_ct = 0 #Range 1-7/8 or 0=max
tic_start = time.perf_counter()
filenames = imaging.take_images()
num_correct = 0

#GET APPROPRIATE QUESTIONS
if (question_source[1] == "1WANS"):
    question_source[1] = read_csv.get_oneword()

if (question_source[1] == "ALL"):
    question_source[1] = read_csv.get_all()

#FOR EACH QUESTION:
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

    #PROCESS TEXT
    question = process_text.process(question)
    answers = process_text.process(answers)
    Process_time = time.perf_counter()

    #LOAD JSON
    site_links = json_data.load(question)
    if (site_links == []):
        print("Q" + str(question_number) + " > (Load JSON Failed) ", end = "")
    JSON_time = time.perf_counter()

    #SEARCH EACH SITE
    if (sites_ct > 0):
        del site_links[sites_ct:]

    if (search_type == "MULTI"):
        search_sites.search_multi(site_links, answers, question_number)
    elif (search_type == "LIN"):
        search_sites.search_lin(site_links, answers, question_number)
    else:
        print("INVALID SEARCH METHOD")

    top_pick = answers[search_sites.get_max()]
    Search_time = time.perf_counter()

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
logging_tool.save_run(total_time, num_correct, len(question_source[1]), search_type)