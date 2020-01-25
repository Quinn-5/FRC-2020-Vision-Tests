import cv2

img = cv2.imread('FIRST.png', cv2.IMREAD_COLOR)

px = img[55, 55]
print(px)
img[55, 55] = [255, 255, 255]
print(px)

img[100:150, 100:150] = [255, 255, 255]

F = img[403:598, 0:166]
for i in range(4):
    img[403:598, (691-166)-134*i:(691-134*i)] = F

cv2.imshow('FIRST', img)

cv2.waitKey(0)
cv2.destroyAllWindows()