
import cv2
import numpy as np
import math
from collections import deque
import argparse




# construct the argument parse
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())




cap = cv2.VideoCapture(-4)
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""

while(cap.isOpened()):
	ret, img = cap.read()   
	cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
	crop_img = img[100:300, 100:300]
	# convert image to grayscale image
	grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	
	
	# convert the grayscale image to binary image
	ret,thresh = cv2.threshold(grey,127,255,0)

	#calculate moments of binary image
	M = cv2.moments(thresh)
	
	value = (35, 35)
	blurred = cv2.GaussianBlur(grey, value, 0)
	_, thresh1 = cv2.threshold(blurred, 127, 255,
							   cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	cv2.imshow('Thresholded', thresh1)
	_,contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
			cv2.CHAIN_APPROX_NONE)
	max_area = -1
	for i in range(len(contours)):
		cnt=contours[i]
		area = cv2.contourArea(cnt)
		if(area>max_area):
			max_area=area
			ci=i
	cnt=contours[ci]
	x,y,w,h = cv2.boundingRect(cnt)
	cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
	hull = cv2.convexHull(cnt)
	drawing = np.zeros(crop_img.shape,np.uint8)
	cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
	cv2.drawContours(drawing,[hull],0,(0,0,255),0)
	hull = cv2.convexHull(cnt,returnPoints = False)
	defects = cv2.convexityDefects(cnt,hull)
	count_defects = 0
	cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)

	# my edit
	
	cnts = cnt
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		if M["m00"] != 0:

			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		else:
	# set values as what you need in the situation
			cX, cY = 0, 0
		if radius > 10:
			# draw the circle and centroid on the img,
			# then update the list of tracked points
			cv2.circle(img, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(img, center, 5, (0, 0, 255), -1)
			pts.appendleft(center)
	# loop over the set of tracked points
	for i in np.arange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# check to see if enough points have been accumulated in
		# the buffer
		if counter >= 10 and i == 1 and pts[-10] is not None:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")
 
			# ensure there is significant movement in the
			# x-direction
			if np.abs(dX) > 20:
				dirX = "East" if np.sign(dX) == 1 else "West"
 
			# ensure there is significant movement in the
			# y-direction
			if np.abs(dY) > 20:
				dirY = "North" if np.sign(dY) == 1 else "South"
 
			# handle when both directions are non-empty
			if dirX != "" and dirY != "":
				direction = "{}-{}".format(dirY, dirX)
 
			# otherwise, only one direction is non-empty
			else:
				direction = dirX if dirX != "" else dirY

				# otherwise, compute the thickness of the line and
		# draw the connecting lines******************
		# thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		# cv2.line(img, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	# show the movement deltas and the direction of movement on
	# the img
	cv2.putText(img, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
	cv2.putText(img, "dx: {}, dy: {}".format(y, y),
		(10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
 
	for i in range(defects.shape[0]):
		s,e,f,d = defects[i,0]
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])
		a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
		b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
		c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
		angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
		if angle <= 90:
			count_defects += 1
			cv2.circle(crop_img,far,1,[0,0,255],-1)
		#dist = cv2.pointPolygonTest(cnt,far,True)
		cv2.line(crop_img,start,end,[0,255,0],2)
		#cv2.circle(crop_img,far,5,[0,0,255],-1)
	if count_defects == 1:
		cv2.putText(img," this is two", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
	elif count_defects == 0:
		str = "this is one"
		cv2.putText(img, str, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
	elif count_defects == 2:
		str = "this is three"
		cv2.putText(img, str, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
	elif count_defects == 3:
		cv2.putText(img,"This is FOUR (:", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
	elif count_defects == 4:
		cv2.putText(img,"THis is Five", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
	else:
		cv2.putText(img,"Center Your hand please, and open it more", (50,50),\
					cv2.FONT_HERSHEY_SIMPLEX, 2, 2)





					
	for i in np.arange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# check to see if enough points have been accumulated in
		# the buffer
		if counter >= 10 and i == 1 and pts[-10] is not None:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")
 
			# ensure there is significant movement in the
			# x-direction
			if np.abs(dX) > 20:
				dirX = "East" if np.sign(dX) == 1 else "West"
 
			# ensure there is significant movement in the
			# y-direction
			if np.abs(dY) > 20:
				dirY = "North" if np.sign(dY) == 1 else "South"
 
			# handle when both directions are non-empty
			if dirX != "" and dirY != "":
				direction = "{}-{}".format(dirY, dirX)
 
			# otherwise, only one direction is non-empty
			else:
				direction = dirX if dirX != "" else dirY

				# otherwise, compute the thickness of the line and
		# draw the connecting lines******************
		# thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		# cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
		# show the movement deltas and the direction of movement on
		# the frame
		cv2.putText(img, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (0, 0, 255), 3)
		cv2.putText(img, "dx: {}, dy: {}".format(y, y),
			(10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
			0.35, (0, 0, 255), 1)






	#cv2.imshow('drawing', drawing)
	#cv2.imshow('end', crop_img)
	cv2.imshow('Gesture Detector', img)
	all_img = np.hstack((drawing, crop_img))
	cv2.imshow('Contours', all_img)
	k = cv2.waitKey(10)
	if k == 27:
		break
