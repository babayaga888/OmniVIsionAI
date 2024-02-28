# import sys
# import os
# from PyQt5.QtCore import Qt, QUrl, QTime
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplitter, QPushButton, QLabel, QListWidget, QListWidgetItem, QStackedWidget, QSlider, QScrollArea
# from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# from PyQt5.QtMultimediaWidgets import QVideoWidget

# class VideoPlayer(QWidget):
#     def __init__(self, video_path, parent=None):
#         super(VideoPlayer, self).__init__(parent)
#         self.video_path = video_path

#         self.initUI()

#     def initUI(self):
#         vbox = QVBoxLayout()

#         self.video_widget = QVideoWidget()
#         self.player = QMediaPlayer()
#         self.player.setVideoOutput(self.video_widget)
#         media_content = QMediaContent(QUrl.fromLocalFile(self.video_path))
#         self.player.setMedia(media_content)

#         vbox.addWidget(self.video_widget)

#         # Create play and pause buttons
#         self.play_button = QPushButton('Play')
#         self.pause_button = QPushButton('Pause')
#         self.play_button.clicked.connect(self.player.play)
#         self.pause_button.clicked.connect(self.player.pause)

#         vbox.addWidget(self.play_button)
#         vbox.addWidget(self.pause_button)

#         # Create a slider for video time frame
#         self.time_slider = QSlider(Qt.Horizontal)
#         self.time_slider.setRange(0, 0)
#         vbox.addWidget(self.time_slider)

#         # Create labels for time frame
#         self.time_label = QLabel('00:00 / 00:00')
#         vbox.addWidget(self.time_label)

#         self.setLayout(vbox)

#         self.player.durationChanged.connect(self.updateDuration)
#         self.player.positionChanged.connect(self.updatePosition)
#         self.time_slider.sliderMoved.connect(self.setPosition)

#     def updateDuration(self, duration):
#         self.duration = duration
#         self.time_slider.setRange(0, duration)

#     def updatePosition(self, position):
#         time = QTime(0, position // 60000, (position // 1000) % 60)
#         total_time = QTime(0, self.duration // 60000, (self.duration // 1000) % 60)
#         self.time_label.setText(f'{time.toString("mm:ss")} / {total_time.toString("mm:ss")}')
#         self.time_slider.setValue(position)

#     def setPosition(self, position):
#         self.player.setPosition(position)

# class VideoList(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.title = "PyQt5 Splitter with Video List"
#         self.top = 200
#         self.left = 500
#         self.width = 800
#         self.height = 600

#         self.initUI()

#     def initUI(self):
#         vbox = QVBoxLayout()

#         # Create a QSplitter for the main window
#         main_splitter = QSplitter(Qt.Horizontal)

#         # Create a QSplitter for the left side (video list and player)
#         left_splitter = QSplitter(Qt.Vertical)

#         self.video_widgets = []
#         self.video_list_widget = QListWidget()
#         self.video_list_widget.setDragDropMode(QListWidget.InternalMove)

#         # Create a stacked widget to hold video players
#         self.stacked_video_players = QStackedWidget()

#         # Select the parent folder containing subfolders with video files
#         parent_folder = r"C:\Users\PC\Desktop\V0.4\recordings"

#         # Iterate through subfolders and their video files
#         if parent_folder and os.path.exists(parent_folder):
#             for root, dirs, files in os.walk(parent_folder):
#                 for file in files:
#                     if file.endswith(('.avi', '.mp4', '.mkv', '.mov')):
#                         video_path = os.path.join(root, file)
#                         video_widget = VideoPlayer(video_path)
#                         self.video_widgets.append(video_widget)

#                         video_name = QLabel(file)
#                         video_name.setAlignment(Qt.AlignCenter)
#                         video_name.setStyleSheet("font-weight: bold;")

#                         # Add video widgets to the stacked widget
#                         self.stacked_video_players.addWidget(video_widget)

#                         video_item = QListWidgetItem()
#                         video_item.setSizeHint(video_name.sizeHint())

#                         folder_name = os.path.basename(root)
#                         video_item.setText(folder_name)
#                         video_item.setFlags(Qt.ItemIsEnabled)

#                         self.video_list_widget.addItem(video_item)

#         left_splitter.addWidget(self.video_list_widget)
#         left_splitter.addWidget(self.stacked_video_players)

#         # Create a QSplitter for the right side (with "Hello, World!" text)
#         right_splitter = QSplitter(Qt.Horizontal)
#         hello_label = QLabel("Hello, World!")
#         hello_label.setAlignment(Qt.AlignCenter)
#         right_splitter.addWidget(hello_label)

#         main_splitter.addWidget(left_splitter)
#         main_splitter.addWidget(right_splitter)

#         vbox.addWidget(main_splitter)
#         self.setLayout(vbox)

#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         self.show()

#         # Connect video list selection to video player display
#         self.video_list_widget.itemClicked.connect(self.videoItemClicked)

#     def videoItemClicked(self, item):
#         index = item.listWidget().row(item)
#         self.stacked_video_players.setCurrentIndex(index)

# if __name__ == '__main__':
#     App = QApplication(sys.argv)
#     window = VideoList()
#     sys.exit(App.exec_())

import sys
import os
from PyQt5.QtCore import Qt, QTimer, QUrl, QIODevice, QObject, QEvent
from PyQt5.QtGui import QImage, QPixmap, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QVideoEncoderSettings
# from moviepy.editor import VideoFileClip
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QScrollArea, QSizePolicy
from PyQt5 import QtCore
import time

from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent, QObject, QSize

class VideoPlayer(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.last_recorded_time = time.time()  # Initialize with the current time
        self.initUI()

    def initUI(self):
        self.mediaPlayer = QMediaPlayer()
        self.video_widget = QVideoWidget(self)

        self.setCentralWidget(self.video_widget)
        self.mediaPlayer.setVideoOutput(self.video_widget)

        self.current_video_index = 0
        self.video_files = []

        # Wait for 60 seconds before starting to check for new videos
        QTimer.singleShot(30000, self.startCheckingVideos)

    def startCheckingVideos(self):
        # Start playing videos as they are recorded
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.playNextVideo)
        self.playNextVideo()
        self.timer.start(2000)  # Check for new videos every 9 seconds

    def playNextVideo(self):
        # Get the latest recorded video
        self.video_files = self.get_video_files(self.path, ".mp4")
        if self.current_video_index < len(self.video_files):
            file_path = os.path.join(self.path, self.video_files[self.current_video_index])

            # Check if the video was recorded after the last recorded time
            video_creation_time = os.path.getctime(file_path)
            if video_creation_time > self.last_recorded_time:
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
                self.mediaPlayer.play()

                self.last_recorded_time = video_creation_time
                self.current_video_index += 1

    def get_video_files(self, folder_path, extension=".mp4"):
        video_files = [f for f in os.listdir(folder_path) if f.endswith(extension)]
        video_files.sort()
        return video_files



            


    def show_frame(self, frame: QImage) -> None:
        
        # Convert QImage to QPixmap and set it as the VideoWidget background
        QPixmap.fromImage(frame)
        self.video_widget.setBackgroundRole(QPalette.Dark)
        self.video_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)      
        # self.video_widget.setScaledContents(True)
        # self.video_widget.setPixmap(pixmap)
       
    
    def updateFrame(self):
        if self.mediaPlayer.state() == QMediaPlayer.State.StoppedState:
            self.playNextVideo()
       
    
    # def updateFrame(self):
    #     if self.mediaPlayer.state() == QMediaPlayer.State.StoppedState:
    #         self.playNextVideo()

    # def handle_worker2_completion(self, final_clip):
    #     # Assuming you have a VideoPlayerWidget to display the video
    #     media_content = QMediaContent(QVideoEncoderSettings(), final_clip)
    #     self.mediaPlayer.setMedia(media_content)
    #     self.mediaPlayer.play()

        # # Get the current frame from MoviePy
        # file_path = os.path.join("C:/Users/PC/Desktop/v0.10/ipcamerarecordings/Section A", self.video_files[self.current_video_index - 1])
        # clip = VideoFileClip(file_path)
        # frame = clip.get_frame(self.mediaPlayer.position() / 1000.0)  # Get frame at the current position

        # Convert the frame to QImage and display it
        # height, width, channel = frame.shape
        # bytesPerLine = 3 * width
        # qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # pixmap = QPixmap.fromImage(qImg)
        # self.videoWidget.setGeometry(0, 0, width, height)
        # self.videoWidget.setPixmap(pixmap)

    # Override method for class MainWindow.
    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """
        Method to capture the events for objects with an event filter installed.
        :param source: The object for whom an event took place.
        :param event: The event that took place.
        :return: True if event is handled.
        """
        #
        if event.type() == QtCore.QEvent.MouseButtonDblClick: # type: ignore
            if source.objectName() == 'Camera_1':
                #
                if self.list_of_cameras_state["Camera_1"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.playback_speed_slider_2.hide()
                    self.playback_speed_slider_3.hide()
                    self.playback_speed_slider_4.hide()
                    self.video_player2.hide()
                    self.video_player3.hide()
                    self.video_player4.hide()
                    self.list_of_cameras_state["Camera_1"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.playback_speed_slider_2.show()
                    self.playback_speed_slider_3.show()
                    self.playback_speed_slider_4.show()
                    self.video_player2.show()
                    self.video_player3.show()
                    self.video_player4.show()
                    self.list_of_cameras_state["Camera_1"] = "Normal"
            elif source.objectName() == 'Camera_2':
                #
                if self.list_of_cameras_state["Camera_2"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.playback_speed_slider_1.hide()
                    self.playback_speed_slider_3.hide()
                    self.playback_speed_slider_4.hide()
                    self.video_player1.hide()
                    self.video_player3.hide()
                    self.video_player4.hide()
                    self.list_of_cameras_state["Camera_2"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.playback_speed_slider_1.show()
                    self.playback_speed_slider_3.show()
                    self.playback_speed_slider_4.show()
                    self.video_player1.show()
                    self.video_player3.show()
                    self.video_player4.show()
                    self.list_of_cameras_state["Camera_2"] = "Normal"
            elif source.objectName() == 'Camera_3':
                #
                if self.list_of_cameras_state["Camera_3"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_4.hide()
                    self.playback_speed_slider_1.hide()
                    self.playback_speed_slider_2.hide()
                    self.playback_speed_slider_4.hide()
                    self.video_player1.hide()
                    self.video_player2.hide()
                    self.video_player4.hide()
                    self.list_of_cameras_state["Camera_3"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_4.show()
                    self.playback_speed_slider_1.show()
                    self.playback_speed_slider_2.show()
                    self.playback_speed_slider_4.show()
                    self.video_player1.show()
                    self.video_player2.show()
                    self.video_player4.show()
                    self.list_of_cameras_state["Camera_3"] = "Normal"
            elif source.objectName() == 'Camera_4':
                #
                if self.list_of_cameras_state["Camera_4"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.playback_speed_slider_1.hide()
                    self.playback_speed_slider_2.hide()
                    self.playback_speed_slider_3.hide()
                    self.video_player1.hide()
                    self.video_player2.hide()
                    self.video_player3.hide()
                    self.list_of_cameras_state["Camera_4"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.playback_speed_slider_1.show()
                    self.playback_speed_slider_2.show()
                    self.playback_speed_slider_3.show()
                    self.video_player1.show()
                    self.video_player2.show()
                    self.video_player3.show()
                    self.list_of_cameras_state["Camera_4"] = "Normal"
            else:
                return super(VideoPlayer, self).eventFilter(source, event)
            return True
        else:
            return super(VideoPlayer, self).eventFilter(source, event)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     player = VideoPlayer("C:/Users/PC/Desktop/v0.10/ipcamerarecordings/Section A")
#     sys.exit(app.exec_())
