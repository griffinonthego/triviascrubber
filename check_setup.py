import numpy as np
import mss.tools
import cv2

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


    # Establish Exit Key
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
