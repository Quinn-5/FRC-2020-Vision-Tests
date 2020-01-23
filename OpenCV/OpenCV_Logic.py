import cv2
import numpy as np

img1 = cv2.imread('3D-Matplotlib.png', cv2.IMREAD_COLOR)
img2 = cv2.imread('mainlogo.png', cv2.IMREAD_COLOR)

# add = img1 + img2
# add = cv2.add(img1, img2)
# weighted = cv2.addWeighted(img1, 0.6, img2, 0.4, 0)

#cv2.imshow('add', weighted)

rows, cols, channels = img2.shape
roi = img1[0:rows, 0:cols]

img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 220, 255, cv2.THRESH_BINARY_INV)

cv2.imshow('mask', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()

cv3.imread