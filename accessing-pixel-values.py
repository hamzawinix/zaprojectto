import cv2
import numpy as numpy
img = cv2.imread('1.jpg')
px = img[100,100]
print (px)
#accessing only blue pixel
blue = img[100,100,0]
print (blue)
#editing
img[100,100] = [255,255,255]
print (img[100,100])
#better accessing
img.item(10,10,2)
#better editing
img.itemset((10,10,2),100)
img.item(10,10,2)
#Total number of pixels is accessed by img.size:
#Image datatype is obtained by img.dtype:
print (img.dtype)