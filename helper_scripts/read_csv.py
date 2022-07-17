import csv
import logging
from helper_scripts import process_text
questions_csv = 'archives/csv/questions.csv'
ocr_destination = 'archives/csv/OCR_dump.csv'

indent = '    '

def open_csv():
    file = open(questions_csv)
    csvreader = csv.reader(file)
    rows = list(csvreader)
    return rows

def get_oneword():
    logger = logging.getLogger(__name__)
    logger.info(indent + "Getting list of 1 word answers...")
    rows = open_csv()

    results = []
    for x in range(1, len(rows)):
        fails = 0
        for y in range(1, len(rows[x]) - 1):
            res = len(rows[x][y].split())
            if (res > 1):
                fails = fails + 1
        if (fails == 0):
            results.append(x)
    results = [x + 1 for x in results]
    # print(" > " + str(results))
    return results

def get_all():
    rows = open_csv()
    results = [*range(2,len(rows)+1)]
    return results

def read_saved_qa(filter):
    logger = logging.getLogger(__name__)
    logger.info(indent + "Getting questions, answers from Q" + str(filter) + " on local csv...")

    rows = open_csv()
    question = rows[filter-1][0]
    answers = [rows[filter-1][1], rows[filter-1][2], rows[filter-1][3]]

    logger.info(2*indent + "Q: " + str(question))
    logger.info(2*indent + "A: " + str(answers))

    return question, answers

def get_correct_ans(search):
    rows = open_csv()
    return rows[search-1][4]

# def get_question_number(question):
#     rows = open_csv()
#
#     for x in range(1, len(rows)):
#         text = process_text.process(rows[x][0])
#         if (text == question):
#             return x
#     return -1

def add_q_and_as(question, answers):
    append = open(ocr_destination, 'a')
    row = question + "," + answers[0] + "," + answers[1] + "," + answers[2] +"\n"
    append.write(row)
