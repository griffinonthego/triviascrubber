import cv2

def shading(q_image):
    q_temp = cv2.imread(q_image)
    pq = cv2.cvtColor(q_temp, cv2.COLOR_BGR2GRAY)
    (thresh, pq) = cv2.threshold(pq, 127, 255, cv2.THRESH_BINARY)
    blur = 5
    pq = cv2.medianBlur(pq, blur)
    return pq