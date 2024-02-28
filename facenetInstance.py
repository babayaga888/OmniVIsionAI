import cv2
import time
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array, array_to_img
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.models import load_model
from numpy import expand_dims


import sys
import typing
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QProgressBar
from PyQt5.QtCore import QThread, QObject, pyqtSignal 
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette
import time
import os
from PyQt5.QtCore import Qt, QTimer, QUrl, QIODevice, QObject, QEvent
from PyQt5.QtGui import QImage, QPixmap, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# from moviepy.editor import VideoFileClip
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QScrollArea, QSizePolicy
from PyQt5 import QtCore
import cv2
# from moviepy.editor import concatenate_videoclips, VideoFileClip
import datetime
from faceReco import Face_embeddings, rename_database
from retinaface import RetinaFace
from keras_facenet import FaceNet
from PIL import Image
from numpy import expand_dims
import numpy as np
from PyQt5.QtCore import QMutex, QMutexLocker
import logging
import threading

class Face_Net:
    def __init__(self, camera_name, new_database, max_distance):
        self.camera_name = camera_name
        self.new_database = new_database
        self.max_distance = max_distance
        self.fourcc = cv2.VideoWriter.fourcc(*'mp4v')

        # Load the FaceNet model
        self.facenet = FaceNet()

        # Dictionary to store video writers for each recognized identity
        self.video_writers = {}

        # Dictionary to store recording start times for each recognized identity
        self.recording_start_times = {}

        logging.basicConfig(filename='accuracy_log.txt', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')


    def start_recording(self, identity, frame):
         if identity not in self.video_writers:
            folder_name = f"recordings/{self.camera_name}/{identity}"  # Modify this line
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{folder_name}/{identity}_{current_time}.mp4"
            self.video_writers[identity] = cv2.VideoWriter(file_name, self.fourcc, 10.0, frameSize=(frame.shape[1], frame.shape[0]))

            return file_name

         return None
    
    

    # def start_recording(self, identity, frame):
    #     if identity not in self.video_writers:
    #         folder_name = f"recordings/{self.camera_name}/{identity}"
    #         if not os.path.exists(folder_name):
    #             os.makedirs(folder_name)

    #         current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #         file_name = f"{folder_name}/{identity}_{current_time}.mp4"
    #         self.video_writers[identity] = cv2.VideoWriter(file_name, self.fourcc, 10.0, frameSize=(frame.shape[1], frame.shape[0]))

    #         return file_name

    #     return None

    def recognize_faces(self, frame):
        fps_start_time = time.time()
        fps_frame_count = 0
        frame_rate = 0
        correct_recognition = 0
        total_frames = 0
        results = RetinaFace.detect_faces(frame)

        if isinstance(results, dict):
            for face_info in results.values():
                facial_area = face_info['facial_area']
                x1, y1, x2, y2 = facial_area
                keypoints = face_info['landmarks']  # Get facial keypoints

                gbr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gbr = Image.fromarray(gbr)
                gbr_array = np.array(gbr, dtype=None, copy=False, order=None)

                face = gbr_array[y1:y2, x1:x2]
                logging.debug('Aligned face dimensions:', face.shape if face is not None else None)

                face = Image.fromarray(face)
                face = face.resize((160, 160))
                face = np.array(face, dtype=None, copy=False, order=None)

                face = expand_dims(face, axis=0)
                signature = self.facenet.embeddings(face)

                print(f"Face Embeddings: {signature}")

                min_dist = 100  # the original minimum distance is 100
                identity = ''

                for key, value in self.new_database.items():
                    dist = np.linalg.norm(value - signature)
                    if dist < min_dist:
                        min_dist = dist
                        identity = key

                if min_dist > self.max_distance:
                    identity = 'stranger'

                if results:
                    fps_frame_count += 1
                    total_frames += 1

                    if identity != '' and identity != 'stranger':
                        correct_recognition += 1

                    recognition_accuracy = (correct_recognition / total_frames) * 100
                    cv2.putText(frame, f'Accuracy: {recognition_accuracy:.2f}%', (10, 60), cv2.FONT_HERSHEY_COMPLEX,
                                1, (255, 255, 0), 2, cv2.LINE_AA)
                    
                    print(f"face recognition Results: {recognition_accuracy}")
                    
                    # Log accuracy to the file
                    logging.info(f"Camera: {self.camera_name} - Identity: {identity} - Accuracy: {recognition_accuracy:.2f}%")

                    # text_position = (x1, y1 - 10)
                    # cv2.putText(frame, identity, text_position, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                    # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    text_position = (x1, y1 - 10)
                    identity_text = f"{identity} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    cv2.putText(frame, identity_text, text_position, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # if fps_frame_count > 0:
                    #     frame_rate = fps_frame_count / (time.time() - fps_start_time)
                    #     cv2.putText(frame, f'FPS: {frame_rate:.2f}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                    #                 (255, 255, 0), 2, cv2.LINE_AA)

                # if identity != '':
                #     if identity not in self.video_writers:
                #         self.start_recording(identity, frame)

                #         self.recording_start_times[identity] = time.time()

                #     if identity == 'stranger' or identity != '':
                #         try:
                #             self.video_writers[identity].write(frame)
                #         except cv2.error as e:
                #             print(f'error writing frame to video')

                #     if identity in self.video_writers and (time.time() - self.recording_start_times[identity]) >= 10:
                #         self.video_writers[identity].release()
                #         del self.video_writers[identity]
                #         del self.recording_start_times[identity]
                # else:
                #     if identity in self.video_writers:
                #         self.video_writers[identity].release()
                #         del self.video_writers[identity]
                #         del self.recording_start_times[identity]

                if identity != '':
                    if identity not in self.video_writers:
                        if identity in self.recording_start_times:
                            elapsed_time = time.time() - self.recording_start_times[identity]
                            if elapsed_time >= 3:
                                self.start_recording(identity, frame)
                                self.recording_start_times[identity] = time.time()

                        else:
                            self.recording_start_times[identity] = time.time()

                    if identity in self.video_writers:
                        try:
                            self.video_writers[identity].write(frame)
                        except cv2.error as e:
                            print(f'error writing frame to video')

                    if identity in self.video_writers and (time.time() - self.recording_start_times[identity]) >= 15: #10
                        self.video_writers[identity].release()
                        del self.video_writers[identity]
                        del self.recording_start_times[identity]
                else:
                    if identity in self.video_writers:
                        self.video_writers[identity].release()
                        del self.video_writers[identity]
                        del self.recording_start_times[identity]

                print(f"Processing {self.camera_name} - {identity}")
                print(f"Identity: {identity}")
                print(f"Face Detection Results: {results}")
        

    