import numpy as np
import cv2

cap = cv2.VideoCapture('vid.webm')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(25) & 0xFF == ord('q'): # change this and the
        # speed of the video changes
        break

cap.release()
cv2.destroyAllWindows()