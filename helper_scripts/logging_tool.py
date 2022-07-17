import csv
import logging
from datetime import datetime

summary = 'archives/logs/run_summary_log.csv'
detail_folder = 'archives/logs/detail/'
global indent
indent = '    '

def configure_logger():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    now = datetime.now()
    dt_string = now.strftime("%m_%d_%Y - %H:%M:%S")
    detail_name = detail_folder + dt_string + ". log"
    latest_name = detail_folder + "latest.log"

    bulk_handler = logging.FileHandler(detail_name)
    latest_handler = logging.FileHandler(latest_name, 'w+')

    # format = "[%(filename)-20s:%(funcName)-20s:%(lineno)-3s] %(message)s"
    # format = "%(message)-50s[%(filename)s:%(funcName)s:%(lineno)s]"
    format = "%(message)-60s%(levelname)s-%(filename)s:%(funcName)s:%(lineno)s"
    format = logging.Formatter(format)

    bulk_handler.setFormatter(format)
    latest_handler.setFormatter(format)

    logger.addHandler(bulk_handler)
    logger.addHandler(latest_handler)

    return logger


def save_run(run_time, num_correct, num_runs, search_type):

    logger = logging.getLogger(__name__)
    logger.info("Saving results to summary file...")
    append = open(summary, 'a')

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    row = [dt_string, run_time, num_correct, num_runs, search_type]
    write = csv.writer(append)
    write.writerow(row)
    append.close()

    logger.info("Finished")
question_number = 22
num_correct = 2
num_runs = 2
run_time = 9.5


