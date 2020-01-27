import pyrealsense2 as pr2
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([255, 255, 255])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('OG', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Filtered', res)

    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        break

    cv2.destroyAllWindows()
    cap.release()
    pipe.stop