import csv
from datetime import datetime

log_file = 'csv_files/logs.csv'

def save_run(run_time, num_correct, num_runs):
    print(str(num_correct) + "/" + str(num_runs))
    append = open(log_file, 'a')

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    row = [dt_string, run_time, num_correct, num_runs]
    write = csv.writer(append)
    write.writerow(row)
    append.close()

question_number = 22
num_correct = 2
num_runs = 2
run_time = 9.5

# num_runs = len(question_source[1])

