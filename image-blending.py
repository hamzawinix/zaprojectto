import cv2
img1 = cv2.imread('2.jpg')
img2 = cv2.imread('02.jpg')
print (img1.shape)
print (img2.shape)


# Read about the resize method parameters here: https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html?highlight=resize#resize
#we  resize becase we cant images of different sizes
img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
dst = cv2.addWeighted(img1, 0.7, img2_resized, 0.3, 0)

print (img1.shape)
print (img2.shape)

cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()