import numpy as np
import cv2
import mss
import mss.tools

# import mss.tools
from PIL import Image
import pytesseract
import time

q_bb = {'top': 140, 'left': 30, 'width': 160, 'height': 110}
qp_bb = {'top': 270, 'left': 30, 'width': 160, 'height': 130}
# a_bb = {'top': 270, 'left': 30, 'width': 160, 'height': 130}

sct = mss.mss()
output = "sct-{top}x{left}_{width}x{height}.png".format(**q_bb)
q_image = "q.png"
pq_image = "pq.png"

cv2.namedWindow("Question")
cv2.moveWindow("Question", 220, 0)

cv2.namedWindow("Question (Processed)")
cv2.moveWindow("Question (Processed)", 220, 250)

# cv2.namedWindow("Question (Processed)")
# cv2.moveWindow("Question (Processed)", 220, 250)

# cv2.resizeWindow("Question", 2000, 1000)

while True:
    q = sct.grab(q_bb)
    cv2.imshow('Question', np.array(q))
    mss.tools.to_png(q.rgb, q.size, output=q_image)

    q_temp = cv2.imread(q_image)
    pq = cv2.cvtColor(q_temp, cv2.COLOR_BGR2GRAY)
    (thresh, pq) = cv2.threshold(pq, 127, 255, cv2.THRESH_BINARY)
    blur = 5
    pq = cv2.medianBlur(pq, blur)
    cv2.imshow('Question (Processed)', pq)
    cv2.imwrite(pq_image, pq)

    ocr_text = pytesseract.image_to_string(Image.open(pq_image));
    print("---OCR--- Blur: " + str(blur) + " \n")
    ocr_text = ocr_text.replace("\n"," ")
    ocr_text = ocr_text.replace("  ", " ")
    print(ocr_text)
    time.sleep(1)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break

    if (cv2.waitKey(1) & 0xFF) == ord('x'):
        ocr_text = pytesseract.image_to_string(Image.open(pq_image));
        print("---OCR--- \n" + ocr_text)

time.sleep(1);
