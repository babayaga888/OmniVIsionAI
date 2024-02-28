import sys
import os
from PyQt5.QtCore import Qt, QUrl, QTime, QThread, pyqtSignal, QEvent, QObject,  QDir
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplitter, QPushButton, QLabel, QListWidget, QListWidgetItem, QStackedWidget, \
    QSlider, QScrollArea,QSizePolicy,QGridLayout, QTreeView, QFileSystemModel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette
from PyQt5 import QtCore
import numpy as np
import cv2
from faceReco import Face_embeddings, rename_database
from retinaface import RetinaFace
from keras_facenet import FaceNet
import time
from PIL import Image
from numpy import expand_dims
import datetime
from PyQt5.QtCore import QSize
import cProfile

database = {}
file_path = r'C:\Users\PC\Desktop\V0.4\DataSetOmniVisionAI-2'
detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5
max_distance = 0.9
video_writers = {}
video_paths = r'C:\Users\PC\Desktop\V0.4\recordings'
recording_start_times = {}


# correct_recognition = 0
# total_frames = 0
new_database = {}

# cap = cv2.VideoCapture(0)




# tracker = DeepSort()#max_age=5, embedder_gpu=True, embedder='mobilenet'

# detector = SSD

facenet = FaceNet()

fourcc = cv2.VideoWriter.fourcc(*'MJPG')


facenet_model = Face_embeddings(file_path, database)


facenet_model.pickle_dump('embeddings')

facenet_model.face_embedding()

facenet_model.pickle_load('embeddings')



rename_database(database, new_database)

class CaptureIpCameraFramesWorker(QThread):
    ImageUpdated = pyqtSignal(QImage)
    
    # recording_started = pyqtSignal(str)
    # recording_stopped = pyqtSignal(str)

    # PlaybackStarted = pyqtSignal(str)
    def __init__(self, url, camera_name) -> None:
        super(CaptureIpCameraFramesWorker, self).__init__()
        self.url = url
        self.__thread_active = True
        self.fps = 0
        self.__thread_pause = False
        self.video_files = {}
        # self.recording_started = False
        # self.recording_stopped = False
        # self.recording_identity = ""
        self.camera_name = camera_name

   
    def start_recording(self, identity, frame):
        # global video_writers, frame_size, fourcc

        global video_writers, fourcc
        if identity not in video_writers:
            folder_name = f"recordings/{self.camera_name}/{identity}"  # Modify this line
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{folder_name}/{identity}_{current_time}.avi"
            video_writers[identity] = cv2.VideoWriter(file_name, fourcc, 10.0, frameSize=(frame.shape[1], frame.shape[0]))

            return file_name

        return None
    
    # def stop_recording(self, identity):
    #     if identity in video_writers:
    #         video_writers[identity].release()
    #         del video_writers[identity]
    #         # Emit signal to indicate recording stopped
    #         # self.recording_stopped.emit(identity)
    
   
    def facial_process(self, frame):
        fps_start_time = time.time()
        fps_frame_count = 0
        frame_rate = 0
        correct_recognition = 0
        total_frames = 0
        results = RetinaFace.detect_faces(frame)
    
        print('result: ', results)

        

        # if time.time() - fps_start_time >= 1.0:
        #         frame_rate = fps_frame_count / (time.time() - fps_start_time)
        #         fps_frame_count = 0
        #         fps_start_time = time.time()
        # cv2.putText(frame, f'FPS: {frame_rate:.2f}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA) 
        if isinstance(results, dict):
            for face_info in results.values():
                facial_area = face_info['facial_area']
                x1, y1, x2, y2 = facial_area
                keypoints = face_info['landmarks']  # Get facial keypoints

                # x1, y1 = abs(x1), abs(y1)
                # x2, y2 = x1 + width, y1 + height

                print(y1, y2, x1, x2)

                gbr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gbr = Image.fromarray(gbr)
                gbr_array = np.array(gbr, dtype=None, copy=False, order=None)

                
                
                face = gbr_array[y1:y2, x1:x2]
                print("Aligned face dimensions:", face.shape if face is not None else None)

                face = Image.fromarray(face)
                face = face.resize((160, 160))
                face = np.array(face, dtype=None, copy=False, order=None) 

                face = expand_dims(face, axis=0)
                signature = facenet.embeddings(face)

                min_dist = 100 #the original minimum distance is 100
                identity = ''

                # detection_info = [
                #     ([result['box'][0], result['box'][1], result['box'][0] + result['box'][2], result['box'][1] + result['box'][3]],
                #     result['confidence'], 'face')
                #     for result in results
                # ]

                # tracks = tracker.update_tracks(detection_info, frame=frame)

                for key, value in new_database.items():
                    dist = np.linalg.norm(value - signature)
                    if dist < min_dist:
                        min_dist = dist
                        identity = key
                        # If the minimum distance is greater than the threshold (max_distance), mark it as stranger
                    if min_dist > max_distance:
                        identity = 'stranger'

                # # If the minimum distance is greater than the threshold (max_distance), mark it as unknown
                # if min_dist > max_distance:
                #     identity = 'stranger'
                

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
                # if identity != '':
                #     start_recording(identity)
                if identity != '':
                    if identity not in video_writers:
                        # Start recording for recognized faces or unknown faces
                        self.start_recording(identity, frame)
                        
                        # Store the current time as the recording start time
                        recording_start_times[identity] = time.time()

                    # Write frame to the video if recording is active
                    if identity == 'stranger' or identity != '':
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
   
    def run(self) -> None:
        # The existing code for capturing IP camera frames goes here
        # ...
        global cap, frame_size

       
        
        # Capture video from a network stream.
        cap = cv2.VideoCapture(self.url)#, cv2.CAP_FFMPEG
        frame_size = (int(cap.get(3)), int(cap.get(4)))
        # Get default video FPS.
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        print(self.fps)
        # If video capturing has been initialized already.q
        if cap.isOpened():
            # While the thread is active.
            while self.__thread_active:
                #
                if not self.__thread_pause:
                    # Grabs, decodes and returns the next video frame.
                    #apply face detection, recognition, and tracking
                 
                    ret, frame = cap.read()

                    # if frame is not None and frame.shape[0]>0 and frame.shape[1]>0:
                    self.facial_process(frame)
                    
                    # If frame is read correctly.
                    if ret: #the original called in if else statement is ret
                        # # Get the frame height, width and channels.
                        height, width, channels = frame.shape

                        # # Calculate the number of bytes per line.
                        bytes_per_line = width * channels
                        # # Convert image from BGR (cv2 default color format) to RGB (Qt default color format).
                        cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # # Convert the image to Qt format.
                        qt_rgb_image = QImage(cv_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        # # Scale the image.
                        # # NOTE: consider removing the flag Qt.KeepAspectRatio as it will crash Python on older Windows machines
                        # # If this is the case, call instead: qt_rgb_image.scaled(1280, 720) 
                        qt_rgb_image_scaled = qt_rgb_image.scaled(1280, 720)  # type: ignore # 720p
                        # # qt_rgb_image_scaled = qt_rgb_image.scaled(1920, 1080, Qt.KeepAspectRatio)
                        # # Emit this signal to notify that a new image or frame is available.
                        
                        self.ImageUpdated.emit(qt_rgb_image_scaled)
                        # height, width, channel = frame.shape
                        # bytes_per_line = channel * width #original is multiplied by 3
                        # rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # q_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        # qt_image_scaled = q_image.scaled(1280, 1080, Qt.KeepAspectRatio) #type: ignore
                        # self.ImageUpdated.emit(qt_image_scaled)
                        #self.video_label.setPixmap(pixmap) # type: ignore
                        # if self.recording_started:
                        #     self.start_recording(self.recording_identity, frame)
                        # elif self.recording_stopped:
                        #     self.stop_recording(self.recording_identity)
                    else:
                        break
               
        #release the video writer
        # for identity in video_writers:
        #  video_writers[identity].release()
        # When everything done, release the video capture object.
        cap.release()
        # Tells the thread's event loop to exit with return code 0 (success).
        self.quit()

    def stop(self) -> None:
        self.__thread_active = False

    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False

    # def start_playback(self, video_path):
    #     self.PlaybackStarted.emit(video_path)

class VideoPlayer(QWidget):
    # PlaybackStarted = pyqtSignal(str)
    def __init__(self, video_path, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.video_path = video_path
        self.duration = 0
        self.initUI()
        

    def initUI(self):
            vbox = QVBoxLayout()

            self.video_widget = QVideoWidget()
            self.player = QMediaPlayer()
            self.player.setVideoOutput(self.video_widget)
            media_content = QMediaContent(QUrl.fromLocalFile(self.video_path))
            self.player.setMedia(media_content)

            vbox.addWidget(self.video_widget)

            # Create play and pause buttons
            self.play_button = QPushButton('Play')
            self.pause_button = QPushButton('Pause')
            self.play_button.clicked.connect(self.playClicked)
            self.pause_button.clicked.connect(self.player.pause)
            # self.player.PlaybackStarted.connect(self.startPlayback)

            vbox.addWidget(self.play_button)
            vbox.addWidget(self.pause_button)

            # Create a slider for video time frame
            self.time_slider = QSlider(Qt.Horizontal) #type: ignore
            self.time_slider.setRange(0, 0)
            vbox.addWidget(self.time_slider)

            # Create labels for time frame
            self.time_label = QLabel('00:00 / 00:00')
            vbox.addWidget(self.time_label)

            self.setLayout(vbox)

            self.player.durationChanged.connect(self.updateDuration)
            self.player.positionChanged.connect(self.updatePosition)
            self.time_slider.sliderMoved.connect(self.setPosition)

    def updateDuration(self, duration):
        self.duration = duration
        self.time_slider.setRange(0, duration)

    def updatePosition(self, position):
        time = QTime(0, position // 60000, (position // 1000) % 60)
        total_time = QTime(0, self.duration // 60000, (self.duration // 1000) % 60)
        self.time_label.setText(f'{time.toString("mm:ss")} / {total_time.toString("mm:ss")}')
        self.time_slider.setValue(position)
        

    def setPosition(self, position):
        self.player.setPosition(position)
    
    def playClicked(self):
        self.player.play()
        # Set the slider style when the video is playing
        self.time_slider.setStyleSheet("QSlider::handle:horizontal { background-color: red; }")
        # self.PlaybackStarted.emit(self.video_path)

    # def startPlayback(self, video_path):
    #     media_content = QMediaContent(QUrl.fromLocalFile(video_path))
    #     self.player.setMedia(media_content)
    #     self.player.play()
    #     self.time_slider.setStyleSheet("QSlider::handle:horizontal { background-color: red; }")

class VideoList(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Splitter with Video List"
        self.top = 200
        self.left = 500
        self.width = 800
        self.height = 600

        # "rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0"


        self.url_1 = "rtsp://admin:hesoyam213@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0"
        self.url_2 = "rtsp://admin:hesoyam213@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0"
        self.url_3 = "rtsp://admin:hesoyam213@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0"
        self.url_4 = "rtsp://admin:hesoyam213@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0"

        # Dictionary to keep the state of a camera. The camera state will be: Normal or Maximized.
        self.list_of_cameras_state = {}

        # Create an instance of a QLabel class to show camera 1.
        self.camera_1 = QLabel()
        self.camera_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_1.setScaledContents(True)
        self.camera_1.installEventFilter(self)
        self.camera_1.setObjectName("Camera_1: Section A")
        self.list_of_cameras_state["Camera_1"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 1 image.
        self.QScrollArea_1 = QScrollArea()
        self.QScrollArea_1.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_1.setWidgetResizable(True)
        self.QScrollArea_1.setWidget(self.camera_1)

        # Create an instance of a QLabel class to show camera 2.
        self.camera_2 = QLabel()
        self.camera_2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_2.setScaledContents(True)
        self.camera_2.installEventFilter(self)
        self.camera_2.setObjectName("Camera_2: Section B")
        self.list_of_cameras_state["Camera_2"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 2 image.
        self.QScrollArea_2 = QScrollArea()
        self.QScrollArea_2.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_2.setWidgetResizable(True)
        self.QScrollArea_2.setWidget(self.camera_2)

        # Create an instance of a QLabel class to show camera 3.
        self.camera_3 = QLabel()
        self.camera_3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_3.setScaledContents(True)
        self.camera_3.installEventFilter(self)
        self.camera_3.setObjectName("Camera_3: Section C")
        self.list_of_cameras_state["Camera_3"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 3 image.
        self.QScrollArea_3 = QScrollArea()
        self.QScrollArea_3.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_3.setWidgetResizable(True)
        self.QScrollArea_3.setWidget(self.camera_3)

        # Create an instance of a QLabel class to show camera 4.
        self.camera_4 = QLabel()
        self.camera_4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_4.setScaledContents(True)
        self.camera_4.installEventFilter(self)
        self.camera_4.setObjectName("Camera_4: Section D")
        self.list_of_cameras_state["Camera_4"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 4 image.
        self.QScrollArea_4 = QScrollArea()
        self.QScrollArea_4.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_4.setWidgetResizable(True)
        self.QScrollArea_4.setWidget(self.camera_4)

        # Set the UI elements for this Widget class.
        self.initUI()

        

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_1 = CaptureIpCameraFramesWorker(self.url_1, 'Section A')
        self.CaptureIpCameraFramesWorker_1.ImageUpdated.connect(lambda image: self.ShowCamera1(image)) # type: ignore

        # # Create an instance of CaptureIpCameraFramesWorker.
        # self.CaptureIpCameraFramesWorker_2 = CaptureIpCameraFramesWorker(self.url_2, 'Section B')
        # self.CaptureIpCameraFramesWorker_2.ImageUpdated.connect(lambda image: self.ShowCamera2(image)) # type: ignore

        # # Create an instance of CaptureIpCameraFramesWorker.
        # self.CaptureIpCameraFramesWorker_3 = CaptureIpCameraFramesWorker(self.url_3, 'Section C')
        # self.CaptureIpCameraFramesWorker_3.ImageUpdated.connect(lambda image: self.ShowCamera3(image)) # type: ignore

        # # Create an instance of CaptureIpCameraFramesWorker.
        # self.CaptureIpCameraFramesWorker_4 = CaptureIpCameraFramesWorker(self.url_4, 'Section D')
        # self.CaptureIpCameraFramesWorker_4.ImageUpdated.connect(lambda image: self.ShowCamera4(image)) # type: ignore




        # Start the thread getIpCameraFrameWorker_1.
        self.CaptureIpCameraFramesWorker_1.start()

        # # Start the thread getIpCameraFrameWorker_2.
        # self.CaptureIpCameraFramesWorker_2.start()

        # # Start the thread getIpCameraFrameWorker_3.
        # self.CaptureIpCameraFramesWorker_3.start()

        # # Start the thread getIpCameraFrameWorker_4.
        # self.CaptureIpCameraFramesWorker_4.start()

   
    def initUI(self):
        vbox = QVBoxLayout()

        # Create a QSplitter for the main window
        main_splitter = QSplitter(Qt.Horizontal)

        # Create a QSplitter for the left side (video list and player)
        left_splitter = QSplitter(Qt.Vertical)

        self.video_widgets = []
        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)

        # Create a stacked widget to hold video players
        self.stacked_video_players = QStackedWidget()

        # Select the parent folder containing subfolders with video files
        parent_folder = r"C:\Users\PC\Desktop\V0.4\recordings"

        # Create a file system model
        model = QFileSystemModel()
        model.setRootPath(parent_folder)
        model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        # Set the model for the tree view
        self.tree_view.setModel(model)
        self.tree_view.setRootIndex(model.index(parent_folder))

        # Handle item selection in the tree view
        self.tree_view.clicked.connect(self.treeItemClicked)

        left_splitter.addWidget(self.tree_view)
        left_splitter.addWidget(self.stacked_video_players)

        # Create a QSplitter for the right side (with "Hello, World!" text)
        grid_layout = QGridLayout()
        right_splitter = QSplitter(Qt.Horizontal)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(self.QScrollArea_1, 0, 0)
        grid_layout.addWidget(self.QScrollArea_2, 0, 1)
        grid_layout.addWidget(self.QScrollArea_3, 1, 0)
        grid_layout.addWidget(self.QScrollArea_4, 1, 1)

        # Create a widget instance.
        self.widget = QWidget(self)
        self.widget.setLayout(grid_layout)
        right_splitter.addWidget(self.widget)
        

        
        
        # right_splitter = QSplitter(Qt.Horizontal)
        # hello_label = QLabel("Hello, World!")
        # hello_label.setAlignment(Qt.AlignCenter)
        # right_splitter.addWidget(grid_layout)

        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(right_splitter)

        vbox.addWidget(main_splitter)
        self.setLayout(vbox)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

        # Connect video list selection to video player display
        # self.video_list_widget.itemClicked.connect(self.videoItemClicked)

    def treeItemClicked(self, index):
        file_info = self.tree_view.model().fileInfo(index)

        if file_info.isFile() and file_info.filePath().endswith(('.avi', '.mp4', '.mkv', '.mov')):
            # Clear existing video players
            # self.stacked_video_players.clear()

            video_path = file_info.filePath()
            video_widget = VideoPlayer(video_path)
            self.stacked_video_players.addWidget(video_widget)

            # Show the video player
            index = self.stacked_video_players.indexOf(video_widget)
            self.stacked_video_players.setCurrentIndex(index)

    def videoItemClicked(self, item):
        index = item.listWidget().row(item)
        self.stacked_video_players.setCurrentIndex(index)

    # @memoize
    # @QtCore.pyqtSlot(QImage)
    # def showCamera(self, frame: QImage) -> None:
    #     current_index = self.stacked_video_players.currentIndex()
    #     self.video_widgets[current_index].setPixmap(QPixmap.fromImage(frame))

 
    @QtCore.pyqtSlot()
    def ShowCamera1(self, frame: QImage) -> None:
        self.camera_1.setPixmap(QPixmap.fromImage(frame))
   
 
    @QtCore.pyqtSlot()
    def ShowCamera2(self, frame: QImage) -> None:
        self.camera_2.setPixmap(QPixmap.fromImage(frame))
    
 
    @QtCore.pyqtSlot()
    def ShowCamera3(self, frame: QImage) -> None:
        self.camera_3.setPixmap(QPixmap.fromImage(frame))
    

    @QtCore.pyqtSlot()
    def ShowCamera4(self, frame) -> None:
        self.camera_4.setPixmap(QPixmap.fromImage(frame))

    def populateRecordedVideosList(self):
        # Assuming recorded videos are stored in the specified directory
        recorded_videos_dir = r'C:\Users\PC\Desktop\V0.4\recordings'
        for root, dirs, files in os.walk(recorded_videos_dir):
            for file in files:
                if file.endswith(".avi"):
                    self.recorded_videos_list.addItem(file)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """
        Method to capture the events for objects with an event filter installed.
        :param source: The object for whom an event took place.
        :param event: The event that took place.
        :return: True if event is handled.
        """
        #
        if event.type() == QtCore.QEvent.MouseButtonDblClick: # type: ignore
            if source.objectName() == 'Camera_1: Section A':
                #
                if self.list_of_cameras_state["Camera_1"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.list_of_cameras_state["Camera_1"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.list_of_cameras_state["Camera_1"] = "Normal"
            elif source.objectName() == 'Camera_2: Section B':
                #
                if self.list_of_cameras_state["Camera_2"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.list_of_cameras_state["Camera_2"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.list_of_cameras_state["Camera_2"] = "Normal"
            elif source.objectName() == 'Camera_3: Section C':
                #
                if self.list_of_cameras_state["Camera_3"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_4.hide()
                    self.list_of_cameras_state["Camera_3"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_4.show()
                    self.list_of_cameras_state["Camera_3"] = "Normal"
            elif source.objectName() == 'Camera_4: Section D':
                #
                if self.list_of_cameras_state["Camera_4"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.list_of_cameras_state["Camera_4"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.list_of_cameras_state["Camera_4"] = "Normal"
            else:
                return super(VideoList, self).eventFilter(source, event)
            return True
        else:
            return super(VideoList, self).eventFilter(source, event)

    # Overwrite method closeEvent from class QMainWindow.
    def closeEvent(self, event) -> None:
        # If thread getIpCameraFrameWorker_1 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_1.isRunning():
            self.CaptureIpCameraFramesWorker_1.quit()
        # # If thread getIpCameraFrameWorker_2 is running, then exit it.
        # if self.CaptureIpCameraFramesWorker_2.isRunning():
        #     self.CaptureIpCameraFramesWorker_2.quit()
        # # If thread getIpCameraFrameWorker_3 is running, then exit it.
        # if self.CaptureIpCameraFramesWorker_3.isRunning():
        #     self.CaptureIpCameraFramesWorker_3.quit()
        # if self.CaptureIpCameraFramesWorker_4.isRunning():
        #     self.CaptureIpCameraFramesWorker_4.quit()
        # # Accept the event
        event.accept()


def main() -> None:
    # Create a QApplication object. It manages the GUI application's control flow and main settings.
    # It handles widget specific initialization, finalization.
    # For any GUI application using Qt, there is precisely one QApplication object
    app = QApplication(sys.argv)
    # Create an instance of the class MainWindow.
    window = VideoList()
    # Show the window.
    window.show()
    # Start Qt event loop.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
