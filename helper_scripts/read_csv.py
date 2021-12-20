import csv


def local(question_number, filename):
    file = open(filename)
    csvreader = csv.reader(file)
    rows = list(csvreader)

    target_row = 1

    print("Question: " + rows[target_row][0])
    print("Answer1: " + rows[target_row][1])
    print("Answer2: " + rows[target_row][2])
    print("Answer3: " + rows[target_row][3])
    print("CorrectAnswer: " + rows[target_row][4])


