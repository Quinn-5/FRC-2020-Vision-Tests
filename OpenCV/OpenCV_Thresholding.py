import cv2

img = cv2.imread('bookpage.jpg')

ret, threshold = cv2.threshold(img, 12, 255, cv2.THRESH_BINARY)

grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, threshold2 = cv2.threshold(img, 12, 255, cv2.THRESH_BINARY)
gaus = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
ret, otsu = cv2.threshold(grayscaled, 125, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)


cv2.imshow('Color', img)
cv2.imshow('Book', threshold)
cv2.imshow('Greyscale', grayscaled)
cv2.imshow('Book2', threshold2)
cv2.imshow('Gaussian', gaus)
cv2.imshow('Otsu', otsu)

cv2.waitKey(0)
cv2.destroyAllWindows()