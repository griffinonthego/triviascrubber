import numpy as np
import mss.tools
import cv2
import process_image, ocr_local, ocr_online
import serpapi

def printarray(array):
    for i in array:
        print(i)

#Create initial question window
q_bb = {'top': 230, 'left': 35, 'width': 300, 'height': 175}
sct = mss.mss()
output = "sct-{top}x{left}_{width}x{height}.png".format(**q_bb)

#Define File Names
q_image = "q.png"
pq_image = "pq.png"

#Arrange Window Locaitions
cv2.namedWindow("Question")
cv2.moveWindow("Question", 360, 0)
cv2.namedWindow("Question (Processed)")
cv2.moveWindow("Question (Processed)", 360, 380)

while True:
    #Get question, Display and save it
    q = sct.grab(q_bb)
    cv2.imshow('Question', np.array(q))
    mss.tools.to_png(q.rgb, q.size, output=q_image)

    #OCR the text from the saved files
    print("Perfoming OCR...")
    method = "online"
    if method == "online":
         ocr_text = ocr_online.ocrify(q_image)
    elif method == "local":
        ocr_text = ocr_local.ocrify(q_image)
    # print("\"" + ocr_text + "\"")

    print("Perfoming Google Search...")
    site_links = serpapi.do_search(ocr_text)
    printarray(site_links)
    print("Searching Sites...")
    search_sites.do_search(site_links)

    break

    #Establish Exit Key
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
