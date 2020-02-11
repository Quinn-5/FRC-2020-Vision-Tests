import cv2
import numpy as np
from math import radians, degrees

def equal(x, y, parallel):
    variance = 5
    Max = x + variance
    Min = x - variance
    if len(parallel):
        for i in parallel:
            X1, Y1, X2, Y2 = i[0]
        
            pSlope = degrees(np.arctan((Y2 - Y1)/(X2 - X1)))
            if not Min < y < Max or Min < pSlope < Max:
                return False
        return True
    else:
        if Min < y < Max:
            return True
            

width = 640
height = 480

img = cv2.imread('Realsense_6_Color.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_color = np.array([70, 80, 255])
upper_color = np.array([95, 180, 255])
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
lines = cv2.HoughLinesP(med_edges, 1, radians(.5), 15, maxLineGap=20)


if lines is not None:
    filtered_lines = []
    for line in lines:
        X1, Y1, X2, Y2 = line[0]
        deg_slope = degrees(np.arctan((Y2 - Y1)/(X2 - X1)))
        if deg_slope < -40 or deg_slope > 40:
            filtered_lines.append(line)


    numLines = len(filtered_lines)
    if numLines > 1:
        parallel = []
        Xtotal = 0
        Ytotal = 0
        for i in range(numLines):
            for j in range(i + 1, numLines):
                iPoints = filtered_lines[i]
                X1, Y1, X2, Y2 = iPoints[0]
                jPoints = filtered_lines[j]
                X3, Y3, X4, Y4 = jPoints[0]
                iSlope = degrees(np.arctan((Y2 - Y1)/(X2 - X1)))
                jSlope = degrees(np.arctan((Y4 - Y3)/(X4 - X3)))

                if equal(iSlope, jSlope, parallel):
                    parallel.append(filtered_lines[i])
                    cv2.line(lineImg, (X1, Y1), (X2, Y2), (0, 255, 0), 1)
                    Xtotal += X1
                    Xtotal += X2
                    Ytotal += Y1
                    Ytotal += Y2
        numLines = len(parallel)
        if numLines:
            Xcenter = Xtotal/(numLines*2)
            Ycenter = Ytotal/(numLines*2)
            lineImg[int(Ycenter), int(Xcenter)] = [255, 255, 255]

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