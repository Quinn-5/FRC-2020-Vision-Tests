import cv2
import numpy as np

width = 640
height = 480

img = cv2.imread('123_Color.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_color = np.array([65, 0, 240])
upper_color = np.array([95, 70, 255])
kernel = np.ones((5, 5), np.uint8)

mask = cv2.inRange(hsv, lower_color, upper_color)

morphMask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

res = cv2.bitwise_and(img, img, mask=morphMask)
blur = cv2.GaussianBlur(mask, (3, 3), 0)
median = cv2.medianBlur(morphMask, 3)

blur_edges = cv2.Canny(blur, 100, 200)
mask_edges = cv2.Canny(mask, 100, 200)
med_edges = cv2.Canny(median, 50, 150)
res_edges = cv2.Canny(res, 100, 200)

lineImg = np.zeros((height, width, 3), np.uint8)
to_radians = np.pi/180
lines = cv2.HoughLinesP(blur_edges, 1, .5 * to_radians, 15, maxLineGap=20)

if lines is not None:
    for line in lines:
        X1, Y1, X2, Y2 = line[0]
        deg_slope = np.arctan((Y2 - Y1)/(X2 - X1))
        if deg_slope < 65 or deg_slope > 125:
            cv2.line(lineImg, (X1, Y1), (X2, Y2), (0, 255, 0), 1)
        cv2.imshow('Lines', lineImg)

cv2.imshow('OG', img)
cv2.imshow('Mask', mask)
cv2.imshow('MorphMask', morphMask)
cv2.imshow('Filtered', res)
cv2.imshow('blur', blur_edges)
cv2.imshow('median', median)
cv2.imshow('med', med_edges)
cv2.imshow('res', res_edges)
cv2.imshow('Mask Edges', mask_edges)

cv2.waitKey(0)

cv2.destroyAllWindows()