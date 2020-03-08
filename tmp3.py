import tmp2
import cv2

cap = cv2.VideoCapture(0)
hist = tmp2.capture_histogram(source=0)

while True:
    ret, frame = cap.read()
    
    # detect the hand
    hand = tmp2.detect_hand(frame, hist)
    
    # plot the fingertips
    for fingertip in hand.fingertips:
        cv2.circle(hand.outline, fingertip, 5, (0, 0, 255), -1)

    cv2.imshow("Handy", hand.outline)
    
    k = cv2.waitKey(5)
    if k == ord('q'):
        break