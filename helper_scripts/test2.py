import collections
import json
import os
import sys
import multiprocessing
import time
import uuid
from pathlib import Path

from nltk.corpus import stopwords

COMMON_WORDS = set(stopwords.words("english"))
BASE_DIR = Path(__file__).resolve(strict=True).parent
DATA_DIR = Path(BASE_DIR).joinpath("data")
OUTPUT_DIR = Path(BASE_DIR).joinpath("output")
PROCESSES = multiprocessing.cpu_count() - 1

def save_file(filename, data):
    random_str = uuid.uuid4().hex
    outfile = f"{filename}_{random_str}.txt"
    with open(Path(OUTPUT_DIR).joinpath(outfile), "w") as outfile:
        outfile.write(data)
    print(Path(OUTPUT_DIR).joinpath(outfile))

def get_word_counts(filename):
    wordcount = collections.Counter()
    # get counts
    with open(Path(DATA_DIR).joinpath(filename), "r") as f:
        for line in f:
            wordcount.update(line.split())
    for word in set(COMMON_WORDS):
        del wordcount[word]

    # save file
    save_file(filename, json.dumps(dict(wordcount.most_common(20))))

    proc = os.getpid()

    print(f"Processed {filename} with process id: {proc}")

def run():
    print(f"Running with {PROCESSES} processes!")

    start = time.time()
    with multiprocessing.Pool(PROCESSES) as p:
        p.map_async(
            get_word_counts,
            [
                "pride-and-prejudice.txt",
                "heart-of-darkness.txt",
                "frankenstein.txt",
                "dracula.txt",
            ],
        )
        # clean up
        p.close()
        p.join()

    print(f"Time taken = {time.time() - start:.10f}")


if __name__ == "__main__":
    run()