import cv2
import numpy as np

img = cv2.imread('FIRST.png', cv2.IMREAD_COLOR)

cv2.line(img, (0,0),  (150, 150), (255, 255, 255), 15)
cv2.rectangle(img, (200, 200), (400, 400), (0, 255, 0), 5)
cv2.circle(img, (100, 50), 55, (0, 0, 255), -1)

pts = np.array([[10, 5],[20, 30],[70, 20],[50, 10]], np.int32)
# pts = pts.reshape((-1, 1, 2))     In docsm kind of redundant
cv2.polylines(img, [pts], True, (0, 255, 255), 3)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV', (0, 130), font, 1, (200, 255, 255), 2, cv2.LINE_AA)

cv2.imshow('Image', img)

cv2.waitKey(0)
cv2.destroyAllWindows()