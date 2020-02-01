import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

while True:
    ret, im = cap.read()
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contour = cv.drawContours(thresh, contours, 3, (0,255,0), 3)

    cv.imshow('img', contour)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cv.waitKey(0)
cv.destroyAllWindows()
