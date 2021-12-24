#TEST CODE ONLY
import search_sites
import load_json
import read_csv
import process_text
import multiprocessing as mp

print("RUNNING TEST.PY")
question_number = 3
question, answers = read_csv.local(question_number)
question = process_text.process(question)
site_links = load_json.load(question)


output = mp.Queue()

# processes = search_sites.search(site_links, answers, question_number)

processes = [mp.Process(target=search_sites.search_multi, args=(site, answers, question_number, output)) for site in site_links]

for p in processes:
    p.start()

for p in processes:
    p.join()

results = [output.get() for p in processes]
print(str(results))
