import csv
from helper_scripts import process_text
questions_csv = 'csv_files/questions.csv'

def open_csv():
    file = open(questions_csv)
    csvreader = csv.reader(file)
    rows = list(csvreader)
    return rows

def get_oneword():
    print("\nGet 1WANS", end = "")
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
    print(" > " + str(results))
    return results

def local(filter):
    # print("\nReading CSV...", end="")
    rows = open_csv()
    question = rows[filter-1][0]
    answers = [rows[filter-1][1], rows[filter-1][2], rows[filter-1][3]]
    return question, answers

def get_correct_ans(search):
    rows = open_csv()
    return rows[search-1][4]

def get_question_number(question):
    rows = open_csv()

    for x in range(1, len(rows)):
        text = process_text.process(rows[x][0])
        if (text == question):
            return x
    return -1

def add_q_and_as(question, answers):
    append = open(questions_csv, 'a')
    row = [question, answers[0], answers[1], answers[2], answers[3]]
    append.write(row)
