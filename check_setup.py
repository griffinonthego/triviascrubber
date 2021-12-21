import numpy as np
import mss.tools
import cv2

q_bb = {'top': 230, 'left': 30, 'width': 300, 'height': 175}
a1_bb = {'top': 450, 'left': 80, 'width': 200, 'height': 50}
a2_bb = {'top': 520, 'left': 80, 'width': 200, 'height': 50}
a3_bb = {'top': 590, 'left': 80, 'width': 200, 'height': 50}

sct = mss.mss()
pdir = 'app_images/'
filenames = {
    'question_image': pdir + 'q.png',
    'processed_question_image': pdir + 'pq.png',
    'answer_image': pdir + 'a.png',
    'processed_answer_image': pdir + 'a.png',
    'answer1_image': pdir + 'a1.png',
    'answer2_image': pdir + 'a2.png',
    'answer3_image': pdir + 'a3.png',
}

# Arrange Window Locaitions
cv2.namedWindow("Question")
cv2.moveWindow("Question", 360, 0)
cv2.namedWindow("a1")
cv2.moveWindow("a1", 360, 380)
cv2.namedWindow("a2")
cv2.moveWindow("a2", 360, 510)
cv2.namedWindow("a3")
cv2.moveWindow("a3", 360, 640)

# Get question, Display and save it
q = sct.grab(q_bb)
a1 = sct.grab(a1_bb)
a2 = sct.grab(a2_bb)
a3 = sct.grab(a3_bb)

cv2.imshow('Question', np.array(q))
cv2.imshow('a1', np.array(a1))
cv2.imshow('a2', np.array(a2))
cv2.imshow('a3', np.array(a3))

mss.tools.to_png(q.rgb, q.size, output=filenames['question_image'])
mss.tools.to_png(a1.rgb, a1.size, output=filenames['answer1_image'])
mss.tools.to_png(a2.rgb, a2.size, output=filenames['answer2_image'])
mss.tools.to_png(a3.rgb, a3.size, output=filenames['answer3_image'])

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

    # Establish Exit Key
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
