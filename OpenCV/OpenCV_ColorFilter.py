import pyrealsense2 as rs2
import cv2
import numpy as np

pipe = rs2.pipeline()
config = rs2.config()
config.enable_stream(rs2.stream.color, 640, 480, rs2.format.bgr8, 30)
profile = pipe.start(config)
s = profile.get_device().query_sensors()[1]
s.set_option(rs2.option.exposure, 163)

while True:
    frames = rs2.composite_frame(pipe.wait_for_frames())
    frame = rs2.video_frame(frames.get_color_frame())
    if not frame:
        continue

    img = np.asanyarray(frame.get_data())

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_color = np.array([65, 0, 240])
    upper_color = np.array([95, 70, 255])

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    morphMask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    res = cv2.bitwise_and(img, img, mask=morphMask)
    median = cv2.medianBlur(res, 3)
    med_edges = cv2.Canny(median, 100, 200)
    res_edges = cv2.Canny(res, 100, 200)

    # cv2.imshow('OG', img)
    # cv2.imshow('Mask', mask)
    # cv2.imshow('MorphMask', morphMask)
    # cv2.imshow('Filtered', res)
    # cv2.imshow('median', median)
    cv2.imshow('med', med_edges)
    cv2.imshow('res', res_edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
pipe.stop()