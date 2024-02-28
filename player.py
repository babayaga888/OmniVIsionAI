from PyQt5.QtCore import Qt, QUrl, QTime, QThread, pyqtSignal, QEvent, QObject,  QDir
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplitter, QPushButton, QLabel, QListWidget, QListWidgetItem, QStackedWidget, \
    QSlider, QScrollArea,QSizePolicy,QGridLayout, QTreeView, QFileSystemModel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette
from PyQt5 import QtCore


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
