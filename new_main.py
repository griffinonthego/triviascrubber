from helper_scripts import ocrify, imaging, gpt3_request
import threading

ocr_type = "ONLINE API"
filenames = imaging.take_images()


question, answers = ocrify.run(ocr_type, filenames)
# question = "Which of these words does NOT only use letters from the top row on the QWERTY keyboard?"
# answers = ['Typewriter', 'Repertoire', 'Prerequisite']

gpt3_request.run(question, answers)

