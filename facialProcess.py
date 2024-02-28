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

facenet = FaceNet()


# def facial_process(self, frame):
#     """Method for facial identification and recognition."""

#     if self.face_clicked: 
#         fps_start_time = time.time()
#         fps_frame_count = 0
#         frame_rate = 0
#         correct_recognition = 0
#         total_frames = 0
#         results = RetinaFace.detect_faces(frame)
    
#         # print('result: ', results)

        

#         # if time.time() - fps_start_time >= 1.0:
#         #         frame_rate = fps_frame_count / (time.time() - fps_start_time)
#         #         fps_frame_count = 0
#         #         fps_start_time = time.time()
#         # cv2.putText(frame, f'FPS: {frame_rate:.2f}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA) 
#         if isinstance(results, dict):
#             for face_info in results.values():
#                 facial_area = face_info['facial_area']
#                 x1, y1, x2, y2 = facial_area
#                 keypoints = face_info['landmarks']  # Get facial keypoints

#                 # x1, y1 = abs(x1), abs(y1)
#                 # x2, y2 = x1 + width, y1 + height

#                 print(y1, y2, x1, x2)

#                 gbr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 gbr = Image.fromarray(gbr)
#                 gbr_array = np.array(gbr, dtype=None, copy=False, order=None)

                
                
#                 face = gbr_array[y1:y2, x1:x2]
#                 logging.debug('Aligned face dimensions:', face.shape if face is not None else None)

#                 face = Image.fromarray(face)
#                 face = face.resize((160, 160))
#                 face = np.array(face, dtype=None, copy=False, order=None) 

#                 face = expand_dims(face, axis=0)
#                 signature = facenet.embeddings(face)

#                 min_dist = 100 #the original minimum distance is 100
#                 identity = ''

#                 # detection_info = [
#                 #     ([result['box'][0], result['box'][1], result['box'][0] + result['box'][2], result['box'][1] + result['box'][3]],
#                 #     result['confidence'], 'face')
#                 #     for result in results
#                 # ]

#                 # tracks = tracker.update_tracks(detection_info, frame=frame)

#                 for key, value in self.new_database.items():
#                     dist = np.linalg.norm(value - signature)
#                     if dist < min_dist:
#                         min_dist = dist
#                         identity = key
#                         # If the minimum distance is greater than the threshold (max_distance), mark it as stranger
#                     if min_dist > self.max_distance:
#                         identity = 'stranger'

#                 # # If the minimum distance is greater than the threshold (max_distance), mark it as unknown
#                 # if min_dist > max_distance:
#                 #     identity = 'stranger'
                

#                 if results:
#                     fps_frame_count += 1
#                     total_frames += 1

#                     if identity != '' and identity != 'stranger':
#                         correct_recognition += 1

#                     recognition_accuracy = (correct_recognition / total_frames) * 100
#                     cv2.putText(frame, f'Accuracy: {recognition_accuracy:.2f}%', (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

#                     # Draw the text on top of the bounding box
#                     text_position = (x1, y1 - 10)
#                     cv2.putText(frame, identity, text_position, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

#                     if fps_frame_count > 0:
#                         frame_rate = fps_frame_count / (time.time() - fps_start_time)

#                         cv2.putText(frame, f'FPS: {frame_rate:.2f}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

#                 # Start recording for recognized faces or unknown faces
#                 # if identity != '':
#                 #     start_recording(identity)
#                 if identity != '':
#                     if identity not in self.video_writers:
#                         # Start recording for recognized faces or unknown faces
#                         self.start_recording(identity, frame)
                        
#                         # Store the current time as the recording start time
#                         self.recording_start_times[identity] = time.time()

#                     # Write frame to the video if recording is active
#                     if identity == 'stranger' or identity != '' : #and self.video_writers
#                         try:
#                             self.video_writers[identity].write(frame)
#                         except cv2.error as e:
#                             print(f'error writing frame to video')

#                     # Check if recording duration is at least 10 seconds
#                     if identity in self.video_writers and (time.time() - self.recording_start_times[identity]) >= 10:
#                         self.video_writers[identity].release()
#                         del self.video_writers[identity]
#                         del self.recording_start_times[identity]
#                 else:
#                     # Stop recording for this identity if it was recording
#                     if identity in self.video_writers:
#                         self.video_writers[identity].release()
#                         del self.video_writers[identity]
#                         del self.recording_start_times[identity]
#                 print(identity)
#     else:
#         print('casual video')

def detect_faces(frame):
    """Method for facial detection using RetinaFace."""
    results = RetinaFace.detect_faces(frame)
    return results

def recognize_faces(frame, results, new_database, max_distance, video_writers, recording_start_times):
    """Method for facial recognition using FaceNet."""
    fps_start_time = time.time()
    fps_frame_count = 0
    frame_rate = 0
    correct_recognition = 0
    total_frames = 0

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
            signature = facenet.embeddings(face)

            min_dist = 100  # the original minimum distance is 100
            identity = ''

            for key, value in new_database.items():
                dist = np.linalg.norm(value - signature)
                if dist < min_dist:
                    min_dist = dist
                    identity = key
                    # If the minimum distance is greater than the threshold (max_distance), mark it as stranger
                if min_dist > max_distance:
                    identity = 'stranger'

            if results:
                fps_frame_count += 1
                total_frames += 1

                if identity != '' and identity != 'stranger':
                    correct_recognition += 1

                recognition_accuracy = (correct_recognition / total_frames) * 100
                cv2.putText(frame, f'Accuracy: {recognition_accuracy:.2f}%', (10, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

                # Draw the text on top of the bounding box
                text_position = (x1, y1 - 10)
                cv2.putText(frame, identity, text_position, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                if fps_frame_count > 0:
                    frame_rate = fps_frame_count / (time.time() - fps_start_time)

                    cv2.putText(frame, f'FPS: {frame_rate:.2f}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

            # Start recording for recognized faces or unknown faces
            if identity != '':
                if identity not in video_writers:
                    # Start recording for recognized faces or unknown faces
                    start_recording(identity, frame, video_writers, recording_start_times)
                    
                    # Store the current time as the recording start time
                    recording_start_times[identity] = time.time()

                # Write frame to the video if recording is active
                if identity == 'stranger' or identity != '' : #and video_writers
                    try:
                        video_writers[identity].write(frame)
                    except cv2.error as e:
                        print(f'error writing frame to video')

                # Check if recording duration is at least 10 seconds
                if identity in video_writers and (time.time() - recording_start_times[identity]) >= 10:
                    video_writers[identity].release()
                    del video_writers[identity]
                    del recording_start_times[identity]
            else:
                # Stop recording for this identity if it was recording
                if identity in video_writers:
                    video_writers[identity].release()
                    del video_writers[identity]
                    del recording_start_times[identity]
            print(identity)
    else:
        print('casual video')

def facial_process(frame, face_clicked, max_distance, new_database, video_writers, recording_start_times):
    """Method for facial identification and recognition."""
    if face_clicked: 
        results = detect_faces(frame)
        recognize_faces(frame, results, new_database, max_distance, video_writers, recording_start_times)
    else:
        print('casual video')
