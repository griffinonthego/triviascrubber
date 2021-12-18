import numpy as np
import time
import mss.tools
import cv2
import process_image, ocr_local, ocr_online, serpapi, search_sites, process_text

def printarray(array):
    for i in array:
        print(i)

#Start timer
tic = time.perf_counter()

#Create initial question window
q_bb = {'top': 230, 'left': 30, 'width': 300, 'height': 175}
# a_bb = {'top': 430, 'left': 30, 'width': 300, 'height': 250}
a1_bb = {'top': 450, 'left': 80, 'width': 200, 'height': 50}
a2_bb = {'top': 520, 'left': 80, 'width': 200, 'height': 50}
a3_bb = {'top': 590, 'left': 80, 'width': 200, 'height': 50}

sct = mss.mss()

#Define File Names
q_image = 'q.png'
pq_image = 'pq.png'
a_image = 'a.png'
pa_image = 'pa.png'
a1_image = 'a1.png'
a2_image = 'a2.png'
a3_image = 'a3.png'

#Arrange Window Locaitions
cv2.namedWindow("Question")
cv2.moveWindow("Question", 360, 0)
# cv2.namedWindow("Answers")
# cv2.moveWindow("Answers", 360, 380)
cv2.namedWindow("a1")
cv2.moveWindow("a1", 360, 380)
cv2.namedWindow("a2")
cv2.moveWindow("a2", 360, 510)
cv2.namedWindow("a3")
cv2.moveWindow("a3", 360, 640)
# cv2.namedWindow("Question (Processed)")
# cv2.moveWindow("Question (Processed)", 360, 380)

while True:
    #Get question, Display and save it
    q = sct.grab(q_bb)
    # a = sct.grab(a_bb)
    a1 = sct.grab(a1_bb)
    a2 = sct.grab(a2_bb)
    a3 = sct.grab(a3_bb)

    cv2.imshow('Question', np.array(q))
    # cv2.imshow('Answers', np.array(a))
    cv2.imshow('a1', np.array(a1))
    cv2.imshow('a2', np.array(a2))
    cv2.imshow('a3', np.array(a3))

    mss.tools.to_png(q.rgb, q.size, output=q_image)
    # mss.tools.to_png(a.rgb, a.size, output=a_image)
    mss.tools.to_png(a1.rgb, a1.size, output=a1_image)
    mss.tools.to_png(a2.rgb, a2.size, output=a2_image)
    mss.tools.to_png(a3.rgb, a3.size, output=a3_image)

    pa = process_image.shading(a_image)
    cv2.imwrite(pa_image, pa)

    #OCR the text from the saved files
    method = "LOCAL"
    print("\nPerfoming OCR... \n\t> Processing Method: " + method)
    answers = ['']*3
    if method == "ONLINE":
         question = ocr_online.ocrify(q_image)
         # answers = ocr_online.ocrify(a_image)
         answers[0] = ocr_online.ocrify(a1_image)
         answers[1] = ocr_online.ocrify(a2_image)
         answers[2] = ocr_online.ocrify(a3_image)
    elif method == "LOCAL":
        question = ocr_local.ocrify(q_image)
        # answers = ocr_local.ocrify(a_image)
        answers[0] = ocr_local.ocrify(a1_image)
        answers[1] = ocr_local.ocrify(a2_image)
        answers[2] = ocr_local.ocrify(a3_image)

    question = process_text.process(question)

    ct = 0
    for i in answers:
        answers[ct] = process_text.process(i)
        ct = ct + 1

    print("\t> Question Result: \"" + question + "\"")
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

    # End timer
    toc = time.perf_counter()
    print(toc-tic)
    break

    # Establish Exit Key
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
