import pyrealsense2 as rs2
import cv2
import numpy as np

width = 640
height = 480

pipe = rs2.pipeline()                           # The camera's API sucks, but at least I can guarantee setings
config = rs2.config()
config.enable_stream(rs2.stream.color, width, height, rs2.format.bgr8, 30)
profile = pipe.start(config)
s = profile.get_device().query_sensors()[1]
s.set_option(rs2.option.brightness, 0)
s.set_option(rs2.option.contrast, 100)
s.set_option(rs2.option.exposure, 45)
s.set_option(rs2.option.gain, 75)
s.set_option(rs2.option.gamma, 100)
s.set_option(rs2.option.hue, 0)
s.set_option(rs2.option.saturation, 50)
s.set_option(rs2.option.sharpness, 0)
s.set_option(rs2.option.white_balance, 2800)

while True:
    frames = rs2.composite_frame(pipe.wait_for_frames())
    frame = rs2.video_frame(frames.get_color_frame())
    if not frame:
        continue

    img = np.asanyarray(frame.get_data())

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_color = np.array([70, 80, 255])
    upper_color = np.array([95, 180, 255])
    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.inRange(hsv, lower_color, upper_color)

    morphMask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    res = cv2.bitwise_and(img, img, mask=morphMask)
    blur = cv2.GaussianBlur(mask, (3, 3), 0)
    median = cv2.medianBlur(morphMask, 3)

    blur_mask = cv2.Canny(blur, 100, 200)
    mask_edges = cv2.Canny(mask, 100, 200)
    med_edges = cv2.Canny(median, 100, 200)
    res_edges = cv2.Canny(res, 100, 200)

    lineImg = np.zeros((height, width, 3), np.uint8)

    to_radians = np.pi/180

    lines = cv2.HoughLines(med_edges, 1, 2.5 * to_radians, 30)

    lines = cv2.HoughLinesP(res_edges, 1, .5 * to_radians, 25, maxLineGap=25)
    x = 0
    if lines is not None:
        for line in lines:
            X1, Y1, X2, Y2 = line[0]
            #deg_slope = np.arctan((Y2 - Y1)/(X2 - X1))
            #if deg_slope < 65 or deg_slope > 125:
            cv2.line(lineImg, (X1, Y1), (X2, Y2), (0, 255, 0), 1)
            cv2.imshow('Lines', lineImg)
            x += 1
        print(str(x))

    cv2.imshow('OG', img)
    cv2.imshow('Mask', mask)
    cv2.imshow('MorphMask', morphMask)
    cv2.imshow('Filtered', res)
    cv2.imshow('blur', blur_mask)
    cv2.imshow('median', median)
    cv2.imshow('med', med_edges)
    cv2.imshow('res', res_edges)
    cv2.imshow('Mask Edges', mask_edges)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
pipe.stop()