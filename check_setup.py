import mss.tools
import cv2
import numpy as np
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

while True:
    #Get question, Display and save it
    q = sct.grab(q_bb)
    a = sct.grab(a_bb)
    cv2.imshow('Question', np.array(q))
    cv2.imshow('Answers', np.array(a))
    mss.tools.to_png(q.rgb, q.size, output=q_image)
    mss.tools.to_png(a.rgb, a.size, output=a_image)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break