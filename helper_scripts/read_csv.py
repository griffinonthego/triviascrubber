import csv
import sys

def open_csv(questions_csv):
    file = open(questions_csv)
    csvreader = csv.reader(file)
    rows = list(csvreader)
    return rows

def get_oneword(questions_csv):
    rows = open_csv(questions_csv)

    results = []
    for x in range(1, len(rows)):
        fails = 0
        for y in range(1, len(rows[x]) - 1):
            res = len(rows[x][y].split())
            if (res > 1):
                fails = fails + 1
        if (fails == 0):
            results.append(x)
    print("\t> Results: " + str(results))

def local(filter, questions_csv):
    rows = open_csv(questions_csv)
    print("\t> Filter: Q" + str(filter))
    question = rows[filter-1][0]
    answers = [rows[filter-1][1], rows[filter-1][2], rows[filter-1][3]]
    return question, answers


def get_correct_ans(search, questions_csv):
    rows = open_csv(questions_csv)
    return rows[search-1][4]



