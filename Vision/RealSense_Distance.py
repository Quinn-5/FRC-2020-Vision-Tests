import pyrealsense2 as rs2
import time

p = rs2.pipeline()

p.start()

while True:
    frames = rs2.composite_frame(p.wait_for_frames())
    depth = rs2.depth_frame(frames.get_depth_frame())

    width = depth.get_height()
    height = depth.get_width()

    dist_to_center = depth.get_distance(int(width / 2), int(height / 2))

    print("The camera is facing an object " + str(dist_to_center) + "meters away")
    # time.sleep(.5)