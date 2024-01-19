import os
import pyrealsense2 as rs
import numpy as np
import cv2

def extract_frames(bag_folder, images_base_folder):
    # Asegurarse de que la carpeta base de imágenes existe
    if not os.path.exists(images_base_folder):
        os.makedirs(images_base_folder)

    # Lista de archivos .bag ordenados por nombre
    bag_files = sorted([file for file in os.listdir(bag_folder) if file.endswith('.bag')])

    # Procesar cada archivo .bag
    for bag_file in bag_files:
        # Configuración de nombres de carpetas y archivos
        bag_path = os.path.join(bag_folder, bag_file)
        images_folder = os.path.join(images_base_folder, bag_file.split('.')[0])
        
        # Crear carpeta para imágenes si no existe
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        # Configura la transmisión desde el archivo .bag
        pipeline = rs.pipeline()
        config = rs.config()
        rs.config.enable_device_from_file(config, bag_path, repeat_playback=False)

        # Inicia el pipeline de RealSense
        pipeline.start(config)
        
        try:
            frame_number = 0
            while True:
                # Espera a que llegue un par coherente de frames: profundidad y color
                frames = pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                if not color_frame:
                    continue

                # Convierte las imágenes a arrays de numpy
                color_image = np.asanyarray(color_frame.get_data())

                # Guarda cada frame como una imagen en la carpeta especificada
                cv2.imwrite(f'{images_folder}/frame_{frame_number:05d}.png', color_image)
                frame_number += 1

        except Exception as e:
            print(f"Se ha producido una excepción: {e}")
        finally:
            # Detiene el pipeline
            pipeline.stop()

        print(f"Frames extraídos guardados en la carpeta: {images_folder}")

# Define la carpeta donde se encuentran los archivos .bag y la carpeta base para las imágenes
bag_folder = r'D:/28Nov/Bags/Todos'
images_base_folder = 'D:/28Nov/Imagenes/ImagenesExtraidasDeLosBag'

# Extrae frames de todos los archivos .bag
extract_frames(bag_folder, images_base_folder)
