import pyrealsense2 as rs
import numpy as np
import cv2

bag_file = '1seg.bag'
output_video_file = 'output_video.avi'

config = rs.config()
rs.config.enable_device_from_file(config, bag_file)
config.enable_stream(rs.stream.color)

pipeline = rs.pipeline()
profile = pipeline.start(config)

stream = profile.get_stream(rs.stream.color)
stream_profile = stream.as_video_stream_profile()
frame_width = stream_profile.width()
frame_height = stream_profile.height()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video_file, fourcc, 30.0, (frame_width, frame_height))

try:
    while True:
        try:
            frames = pipeline.wait_for_frames()
        except RuntimeError:
            # Se lanza una excepción cuando se alcanza el final del archivo .bag
            print("Reached end of the bag file.")
            break

        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        out.write(color_image)

except Exception as e:
    print(e)
finally:
    out.release()
    pipeline.stop()
