import pyrealsense2 as rs2
import numpy as np
import cv2

# Configuration
pipe = rs2.pipeline()       # Setup pipeline
config = rs2.config()
config.enable_stream(rs2.stream.infrared, 640, 480, rs2.format.y8, 30)  # Start Color Stream
config.enable_stream(rs2.stream.depth, 640, 480, rs2.format.z16, 30)    # Start Depth Stream
config.enable_stream(rs2.stream.color, 640, 480, rs2.format.bgr8, 30)   # Start Color Stream
# print(rs2.options.get_option(rs2.option))

# Start Streaming
pipe.start(config)

try:
    while True:

        # Wait for coherent pair of frames: Depth and Color
        frames = rs2.composite_frame(pipe.wait_for_frames())
        ir_frame = rs2.video_frame(frames.get_infrared_frame())
        depth_frame = rs2.depth_frame(frames.get_depth_frame())
        color_frame = rs2.video_frame(frames.get_color_frame())
        if not ir_frame or not depth_frame or not color_frame:      #TODO: check if this is actually useful
            continue

        # Convert images to numpy arrays
        ir_image = np.asanyarray(ir_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first for compatibility, may be left alone for analysis)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Threshold and greyscale operations
        # greyscale = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        # ret, CThresh = cv2.threshold(greyscale, 225, 255, cv2.THRESH_BINARY_INV)
        # ret, IRThresh = cv2.threshold(ir_image, 240, 255, cv2.THRESH_BINARY_INV)

        #get frame size
        width = depth_frame.get_height()
        height = depth_frame.get_width()
        dist_to_center = depth_frame.get_distance(int(width / 2), int(height / 2))

        XCenter = int(width/2)
        YCenter = int(height/2)

        # Drawing lines and text for distance
        cv2.line(depth_colormap, (XCenter, 0), (XCenter, height), (255, 255, 255), 1)
        cv2.line(depth_colormap, (0, YCenter), (width, YCenter), (255, 255, 255), 1)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(depth_colormap, str(dist_to_center), (XCenter, YCenter), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Show images
        # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('RealSense', images)
        # cv2.imshow('Color', color_image)
        # cv2.imshow('Greyscale', CThresh)
        cv2.imshow('Depth', depth_colormap)
        # cv2.imshow('IR', ir_image)
        # cv2.imshow('IRTthresh', IRThresh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:

    pipe.stop()