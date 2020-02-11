import numpy as np

# Guess who knows how to iterate through a list?
# It felt much more daunting than it actually was, don't judge...

def equal(x1, y1, x2, y2):
    variance = 5
    xmax = x1 + variance
    xmin = x1 - variance
    ymax = y1 + variance
    ymin = y1 - variance
    if xmin < x2 < xmax and ymin < y2 < ymax:
        return True
    else:
        return False

x = np.array(
    [[[181, 277, 205, 239]],
     [[206, 239, 248, 242]],
     [[199, 247, 253, 251]],
     [[189, 280, 215, 239]],
     [[250, 244, 267, 277]],
     [[244, 252, 260, 283]]],
    dtype=np.int32)

numLines = len(x)

intersects = []

for i in range(numLines):
    print(i)
    print(x[i])

    for j in range(i + 1, numLines):    # Get points, FOIL it (sorta)
        print(x[j])
        iPoints = x[i]
        x1, y1, x2, y2 = iPoints[0]
        jPoints = x[j]
        x3, y3, x4, y4 = jPoints[0]
        if equal(x1, y1, x3, x3):       # First
            intersects.append([x1, y1])
        if equal(x1, y1, x4, y4):       # Outer
            intersects.append([x1, y1])
        if equal(x2, y2, x3, y3):       # Inner
            intersects.append([x2, y2])
        if equal(x2, y2, x4, y4):       # Last
            intersects.append([x2, y2])

    print(intersects)