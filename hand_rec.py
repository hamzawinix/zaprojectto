

#tHIS CODE VERSION IS NOT WORKING









import cv2 
import imutils
import numpy as np


#global 

bg = None
def run_avg(image, aWeight):
    global bg 
     #background calling
    if bg is None:
        bg = image.copy().astype("float")
        return
    #computing the weighted average ,accumelating it and updating the background
    cv2.accumulateWeighted(image, bg ,aWeight)

#now to segment the region of hand in image
def segment (image, threshold=25):
    global bg
    #finding difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), image)

    #threshold the diff image so we extact the foreground
    threshold = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    thresholdcopy = threshold.copy
    #getting countours in the new threshold image 
    contours, hierarchy = cv2.findContours(thresholdcopy[0], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #if no countours found return None 
    if len(cnts) == 0 :
        return
    else :
        #get the maximum countour which is the hand (based on the contour area )
        segmented = max(cnts, key = cv2.contourArea)
        return (threshold, segmented)

#main Function
if __name__ == "__main__": 

    #initialize weight for running average
    aWeight = 0.5

    # get the refrence to the webcam
    camera = cv2.VideoCapture(-1) #might need to change for ras

    # region of intrest (ROI) cordinates
    top, right, bottom, left = 10, 350, 225, 590

    #initialize num of frames
    num_frames = 0

    #keep loooing  until interpreted 
    while (True):

        #get the current frame 
        (grapped, frame) = camera.read()

        #resize the frame 
        frame = imutils.resize(frame, width=700)

        #flip the frame to make sure its not mirrored 
        frame = cv2.flip (frame, 1)

        # clone the fram e 
        clone = frame.copy()

        #get the height and width of the frame 
        (height, width) = frame .shape[:2]

        #get the ROI
        roi = frame [top: bottom, right: left ]

        #convert the roi to grayscale and blur it 
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)



#hereeeeeeeeeeeeeee

         # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        if num_frames < 30:
            run_avg(gray, aWeight)
        else:
            # segment the hand region
            hand = segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented) = hand

                # draw the segmented region and display the frame
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                cv2.imshow("Thesholded", thresholded)

        # draw the segmented hand
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)

        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

# free up memory
camera.release()
cv2.destroyAllWindows()














