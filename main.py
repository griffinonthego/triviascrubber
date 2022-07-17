import time
import sys
import logging
from helper_scripts import ocrify, imaging, search_sites, json_data, read_csv, process_text, logging_tool
indent = '    '

logging_tool.configure_logger()
logger = logging.getLogger(__name__)

#SETUP (1WANS -> [3, 4, 5, 6, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
question_source = ["CSV", range(2,3)] # ["OCR"] OR ["CSV", *question_number* OR "1WANS" OR "ALL"]]
ocr_source = "LOCAL"
ocr_type = "ONLINE API" #LOCAL or ONLINE API
search_type = "multithreaded" #multithreaded OR linear
sites_ct = 0 #Range 1-7/8 or 0=max
tic_start = time.perf_counter()
filenames = imaging.take_images()
num_correct = 0

# logger.info("Listing parameters..."
#                     "\n" + space + "\tquestion_source: " + str(question_source) +
#                     "\n" + space + "\tsearch_type: " + str(search_type))

logger.info("Running main script...")

#GET APPROPRIATE QUESTIONS
if (question_source[1] == "1WANS"):
    question_source[1] = read_csv.get_oneword()
elif (question_source[1] == "ALL"):
    question_source[1] = read_csv.get_all()

#FOR EACH QUESTION:
for question_number in question_source[1]:
    question_start_tic = time.perf_counter()

    #GET TEXT
    if (question_source[0] == "OCR"):
        question, answers = ocrify.run(ocr_type, filenames)
    elif (question_source[0] == "CSV"):
        question, answers = read_csv.read_saved_qa(question_number)
    else:
        logger.ERROR("INVALID QUESTION SOURCE")

    OCR_time = time.perf_counter()
    logger.info(indent*2 + "Section time:" +  str(round((OCR_time - question_start_tic), 2)))
    tic = time.perf_counter()

    #PROCESS TEXT
    logger.info(indent*1 + "Processing text...")
    question = process_text.process(question)
    answers = process_text.process(answers)

    Process_time = time.perf_counter()
    logger.info(indent*2 + "Section time:" +  str(round((Process_time - tic), 2)))
    tic = time.perf_counter()

    #LOAD JSON
    logger.info(indent*1 + "Gathering website links...")
    site_links = json_data.local_load(question_number)

    JSON_load_time = time.perf_counter()
    logger.info(indent*2 + "Section time:" +  str(round((JSON_load_time - tic), 2)))
    tic = time.perf_counter()

    #FILTER SITES
    logger.info(indent*1 + "Filtering bad links...")
    if (sites_ct > 0):
        del site_links[sites_ct:]
    site_links = search_sites.filter_bad_sites(site_links)

    Filter_site_site = time.perf_counter()
    logger.info(indent*2 + "Section time:" + str(round((Filter_site_site - tic), 2)))
    tic = time.perf_counter()

    #SEARCH EACH SITE
    logger.info(indent*1 + "Running website load/search (" + search_type + ")...")
    if (search_type == "multithreaded"):
        search_sites.search_multi(site_links, answers, question_number)
    elif (search_type == "linear"):
        search_sites.search_lin(site_links, answers, question_number)
    else:
        logger.error("Invalid load/search method")

    top_pick = answers[search_sites.get_max()]
    print(top_pick)
    Search_time = time.perf_counter()
    logger.info(indent*2 + "Section time:" +  str(round((Search_time - JSON_load_time), 2)))

    #
    # #CHECK ANSWER IF CSV USED
    # if (question_source[0] == "CSV"):
    #     correct_ans = read_csv.get_correct_ans(question_number)
    #     correct_ans = process_text.process(correct_ans)
    #
    #     if (correct_ans == top_pick):
    #         print(" > Correct", end = "")
    #     else:
    #         print(" > Incorrect", end = "")
    #
    #     if (top_pick == process_text.process(correct_ans)):
    #         num_correct = num_correct + 1
    #
    # #END
    # toc = time.perf_counter()
    # print("\t(" + str(round((toc-tic),2)) + " sec)", end="\n")

final_toc = time.perf_counter()
total_time = str(round((final_toc-tic_start), 2))
logging_tool.save_run(total_time, num_correct, len(question_source[1]), search_type)