import numpy as np
import time
import mss.tools
import cv2
import process_image, ocr_local, ocr_online, serpapi, search_sites, process_text


def printarray(array):
    for i in array:
        print(i)

#Create initial question window
q_bb = {'top': 230, 'left': 30, 'width': 300, 'height': 175}
a_bb = {'top': 430, 'left': 30, 'width': 300, 'height': 250}
sct = mss.mss()

#Define File Names
q_image = "q.png"
pq_image = "pq.png"
a_image = "a.png"


#Arrange Window Locaitions
cv2.namedWindow("Question")
cv2.moveWindow("Question", 360, 0)
cv2.namedWindow("Answers")
cv2.moveWindow("Answers", 360, 380)
# cv2.namedWindow("Question (Processed)")
# cv2.moveWindow("Question (Processed)", 360, 380)

while True:
    #Get question, Display and save it
    q = sct.grab(q_bb)
    a = sct.grab(a_bb)
    cv2.imshow('Question', np.array(q))
    cv2.imshow('Answers', np.array(a))
    mss.tools.to_png(q.rgb, q.size, output=q_image)
    mss.tools.to_png(a.rgb, a.size, output=a_image)



    #OCR the text from the saved files
    method = "LOCAL"
    print("\nPerfoming OCR... \n\t> Processing Method: " + method)
    if method == "ONLINE":
         question = ocr_online.ocrify(q_image)
         answers = ocr_online.ocrify(a_image)
    elif method == "LOCAL":
        question = ocr_local.ocrify(q_image)
        answers = ocr_local.ocrify(a_image)
    question = process_text.process(question)
    answers = process_text.process(answers)

    print("\t> Question Result: \"" + question + "\"")
    answers = answers.split(' ')
    print("\t> Answers Result: " + str(answers))

    print("Perfoming Google Search...")
    site_links = serpapi.do_search(question)
    while('' in site_links):
        site_links.remove('')

    print("Searching Sites...")
    appearences = [0, 0, 0]
    for site in site_links:
        appearences = np.add(appearences, search_sites.do_search(site,answers))

    ct = 0
    for i in answers:
        print(str(i) + ": " + str(appearences[ct]))
        ct = ct + 1

    break

    # Establish Exit Key
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
