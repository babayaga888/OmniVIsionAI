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
from facenetInstance import Face_Net


class CaptureIpCameraFramesWorker(QThread):
    logging.debug('Starting the run method...')
    # Signal emitted when a new image or a new frame is ready.
    
    ImageUpdated = pyqtSignal(QImage)

    def __init__(self, url, output_filename, camera_name) -> None:
        super(CaptureIpCameraFramesWorker, self).__init__()
        # Declare and initialize instance variables.
        self.isInitialized = False
        self.url = url
        self.__thread_active = True
        self.fps = 0
        self.__thread_pause = False
        self.output_filename = output_filename
        self.camera_name = camera_name
        self.frame_queue = []
        self.start_rec = 0
        self.recording_active = False
        self.video_writers = {}
        self.facenet = FaceNet()
        self.new_database = {}
        self.max_distance = 0.9
        self.recording_start_times = {}
        self.database = {}
        self.file_path = r'add faces of participants here for facial embeddings'
        self.mutex = QMutex()
        self._current_frame = None
        # self.facenet_models = {}
        self.face_clicked = False

        
       
        
        # Initialize facenet model for this camera
        self.facenet_models = Face_embeddings(self.file_path, self.database)
        self.facenet_models.pickle_dump('embeddings')
        self.facenet_models.face_embedding()
        self.facenet_models.pickle_load('embeddings')


        # Initialize Face_Net instance with an empty new_database
        # self.fn = Face_Net(self.camera_name, {}, self.max_distance)

        # Rename the database and update the new_database in Face_Net
        rename_database(self.database, self.new_database)

        self.fn = Face_Net(self.camera_name, self.database, self.max_distance)

        self.video_path = r'C:\Users\PC\Desktop\v0.10\ipcamerarecordings\Section A'

    
        
    # def start_recording(self, identity, frame):
    #     # global video_writers, frame_size, fourcc

    #     # global self.video_writers, fourcc
    #     if identity not in self.video_writers:
    #         folder_name = f"recordings/{self.camera_name}/{identity}"  # Modify this line
    #         if not os.path.exists(folder_name):
    #             os.makedirs(folder_name)

    #         current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #         file_name = f"{folder_name}/{identity}_{current_time}.mp4"
    #         self.video_writers[identity] = cv2.VideoWriter(file_name, self.fourcc, 10.0, frameSize=(frame.shape[1], frame.shape[0]))

    #         return file_name

    #     return None
        
    def run(self) -> None:
   
        # Capture video from a network stream.
        self.cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)

        
        
        # Get default video FPS.
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        print(self.fps)
        # If video capturing has been initialized already.q
        if self.cap.isOpened():
            # While the thread is active.
            folder_path = os.path.join("ipcamerarecordings", self.camera_name)
            os.makedirs(folder_path, exist_ok=True)

            if self.output_filename:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                self.output_path = os.path.join(folder_path, f"{self.output_filename}_{timestamp}.mp4")
                self.fourcc = cv2.VideoWriter.fourcc(*'mp4v')
                self.frame_width = int(self.cap.get(3))
                self.frame_height = int(self.cap.get(4))
                self.video_writer = cv2.VideoWriter(self.output_path, self.fourcc, self.fps, (self.frame_width, self.frame_height))
            

            self.start_time = time.time()
            recording_duration = 5 #10
            while self.__thread_active:
                #
                if not self.__thread_pause:
                    # Grabs, decodes and returns the next video frame.
                    ret, frame = self.cap.read()
                    logging.debug('Frame read successfully...')
                              
                    if ret:
                      
                   
                       if self.face_clicked: 
                          self.fn.recognize_faces(frame)
                        
                       self.frame_queue.append(frame)
                       self.process_frame()
                       self.current_frame = frame
                       logging.debug('Frame processed successfully...')
                       

                       elapsed_time = time.time() - self.start_time
                       if elapsed_time >= recording_duration and not self.recording_active:
                            self.start_recordings(self.camera_name)

                       if elapsed_time >= 2 * recording_duration and self.recording_active:
                            self.stop_recordings()
                            self.start_time = time.time()
                    else:
                        logging.error('Error reading frame...')
                        break
        # When everything done, release the video capture object.
        # cap.release()
        # if self.video_writer:
        #     self.video_writer.release()

        self.cap.release()
        # Tells the thread's event loop to exit with return code 0 (success).
        self.quit()

   
    # def facial_process(self, frame):
    #    """Method for facial identification and recognition."""

    #    if self.face_clicked: 
    #         fps_start_time = time.time()
    #         fps_frame_count = 0
    #         frame_rate = 0
    #         correct_recognition = 0
    #         total_frames = 0
    #         results = RetinaFace.detect_faces(frame)
        
    #         # print('result: ', results)

            

        
    #         if isinstance(results, dict):
    #             for face_info in results.values():
    #                 facial_area = face_info['facial_area']
    #                 x1, y1, x2, y2 = facial_area
    #                 keypoints = face_info['landmarks']  # Get facial keypoints

              

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
    #                 signature = self.facenet.embeddings(face)

    #                 print(f"Face Embeddings: {signature}")


    #                 min_dist = 100 #the original minimum distance is 100
    #                 identity = ''

                    

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
    #                 # print(identity)
    #                 print(f"Processing {self.camera_name} - {identity}")
    #                 print(f"Identity: {identity}")
    #                 print(f"Face Detection Results: {results}")

    # #    else:
    # #     # print('casual video')


    def process_frame(self):
        
        
        while len(self.frame_queue) > 0:
            frame = self.frame_queue.pop(0)

            height, width, channels = frame.shape
            bytes_per_line = width * channels
            cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qt_rgb_image = QImage(cv_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            qt_rgb_image_scaled = qt_rgb_image.scaled(1280, 720, Qt.KeepAspectRatio) # type: ignore

            self.ImageUpdated.emit(qt_rgb_image_scaled)

            
            self.video_writer.write(frame)

            

    def start_recordings(self, camera_name):
        logging.debug('Starting recordings...')
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.output_path = os.path.join(self.video_path, f"{self.output_filename}_{timestamp}.mp4")
        self.fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.video_writer = cv2.VideoWriter(self.output_path, self.fourcc, self.fps, (self.frame_width, self.frame_height))
        self.video_writers[camera_name] = self.video_writer
    
        self.recording_active = True

    def stop_recordings(self):
        logging.debug('Stopping recordings...')
        if self.video_writer:
            self.video_writer.release()
            self.recording_active = False

    

    def stop(self) -> None:
        self.__thread_active = False
  
    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False

  
