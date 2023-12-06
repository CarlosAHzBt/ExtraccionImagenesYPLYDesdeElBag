import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time

bag_file = '1seg.bag'
color_folder = 'color_frames'
ply_folder = 'ply_files'
os.makedirs(color_folder, exist_ok=True)
os.makedirs(ply_folder, exist_ok=True)

config = rs.config()
rs.config.enable_device_from_file(config, bag_file, repeat_playback=False)
config.enable_stream(rs.stream.depth)
config.enable_stream(rs.stream.color)

pipeline = rs.pipeline()
profile = pipeline.start(config)
align_to = rs.stream.color
align = rs.align(align_to)

frame_count = 0
timeout_ms = 5000  # Tiempo de espera en milisegundos

try:
    while True:
        try:
            frames = pipeline.wait_for_frames(timeout_ms)
        except RuntimeError:
            print("Timeout occurred, no more frames.")
            break

        frame_count += 1

        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        cv2.imwrite(f'{color_folder}/color_frame_{frame_count}.png', color_image)

        ply_filename = f'{ply_folder}/frame_{frame_count}.ply'
        points = rs.pointcloud()
        points.map_to(color_frame)
        v = points.calculate(aligned_depth_frame)
        v.export_to_ply(ply_filename, color_frame)

        print(f'Frame {frame_count} processed.')

        time.sleep(0.01)  # Retardo para dar tiempo a que los datos estén listos

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    pipeline.stop()
