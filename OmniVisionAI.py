from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QScrollArea, QSizePolicy,QDialog, QFrame, QHeaderView, \
    QLineEdit, QHBoxLayout, QTreeWidget
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent, QObject, QSize, QSortFilterProxyModel
from PyQt5 import QtCore,uic
import sys
from PyQt5.QtWidgets import QSlider, QVBoxLayout
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
# from exp import VideoPlayer
from workers import  CaptureIpCameraFramesWorker

from exp import VideoPlayer

from PyQt5.QtCore import Qt, QUrl, QTime, QThread, pyqtSignal, QEvent, QObject,  QDir, QModelIndex
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplitter, QPushButton, QLabel, QListWidget, QListWidgetItem, QStackedWidget, \
    QSlider, QScrollArea,QSizePolicy,QGridLayout, QTreeView, QFileSystemModel, QMainWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette
from PyQt5 import QtCore
from player import VideoPlayer
import file_sort as file_sort
from PyQt5.QtCore import Qt, QObject, QEvent, QThread, pyqtSignal, pyqtSlot, QDir
from facenetInstance import Face_Net

class FaceManager:
    def __init__(self):
        # Create a dictionary to store FaceNet instances for each camera
        self.face_nets = {}

    def add_camera(self, camera_name, new_database, max_distance):
        # Create a Face_Net instance for the specified camera
        self.face_nets[camera_name] = Face_Net(camera_name, new_database, max_distance)

    def recognize_faces_for_camera(self, camera_name, frame):
        # Use the Face_Net instance corresponding to the camera_name
        return self.face_nets[camera_name].recognize_faces(frame)
class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super(MainWindow, self).__init__()

      
        self.url_1 = "rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0"
        self.url_2 = "rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0"
        self.url_3 = "rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0"
        self.url_4 = "rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0"

        # Dictionary to keep the state of a camera. The camera state will be: Normal or Maximized.
        self.list_of_cameras_state = {}

        # Create an instance of a QLabel class to show camera 1.
        self.camera_1 = QLabel()
        self.camera_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_1.setScaledContents(True)
        self.camera_1.installEventFilter(self)
        self.camera_1.setObjectName("Camera_1")
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
        self.camera_2.setObjectName("Camera_2")
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
        self.camera_3.setObjectName("Camera_3")
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
        self.camera_4.setObjectName("Camera_4")
        self.list_of_cameras_state["Camera_4"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 4 image.
        self.QScrollArea_4 = QScrollArea()
        self.QScrollArea_4.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_4.setWidgetResizable(True)
        self.QScrollArea_4.setWidget(self.camera_4)

        # Set the UI elements for this Widget class.
        self.__SetupUI()

        # # Create an instance of CaptureIpCameraFramesWorker.
        # self.CaptureIpCameraFramesWorker_1 = CaptureIpCameraFramesWorker(self.url_1, 'Section_A_Recording', 'Section A')
        # self.CaptureIpCameraFramesWorker_1.ImageUpdated.connect(lambda image: self.ShowCamera1(image))

        # # Create an instance of CaptureIpCameraFramesWorker.
        # self.CaptureIpCameraFramesWorker_2 = CaptureIpCameraFramesWorker(self.url_2, 'Section_B_Recording', 'Section B')
        # self.CaptureIpCameraFramesWorker_2.ImageUpdated.connect(lambda image: self.ShowCamera2(image))

        # # Create an instance of CaptureIpCameraFramesWorker.
        # self.CaptureIpCameraFramesWorker_3 = CaptureIpCameraFramesWorker(self.url_3,'Section_C_Recording', 'Section C')
        # self.CaptureIpCameraFramesWorker_3.ImageUpdated.connect(lambda image: self.ShowCamera3(image))

        # # Create an instance of CaptureIpCameraFramesWorker.
        # self.CaptureIpCameraFramesWorker_4 = CaptureIpCameraFramesWorker(self.url_4,'Section_D_Recording', 'Section D')
        # self.CaptureIpCameraFramesWorker_4.ImageUpdated.connect(lambda image: self.ShowCamera4(image))
        
        # Create an instance of FaceManager
        
        # self.new_databases = {}
        # self.max_distances = 0.9

        # self.face_manager = FaceManager()

        # # Add cameras to the FaceManager
        # for camera_name in ["Section A", "Section B"]:
        #     self.face_manager.add_camera(camera_name, self.new_databases, self.max_distances)

        # Create an instance of CaptureIpCameraFramesWorker
        self.CaptureIpCameraFramesWorker_1 = CaptureIpCameraFramesWorker(url=self.url_1, output_filename='Section_A_Recording', camera_name='Section A')

        # Connect the signal from worker to the slot method
        self.CaptureIpCameraFramesWorker_1.ImageUpdated.connect(lambda image: self.ShowCamera1(image))

        # Start the worker thread
        self.CaptureIpCameraFramesWorker_1.start()

         # Create an instance of CaptureIpCameraFramesWorker
        self.CaptureIpCameraFramesWorker_2 = CaptureIpCameraFramesWorker(url=self.url_2, output_filename='Section_B_Recording', camera_name='Section B')

        # Connect the signal from worker to the slot method
        self.CaptureIpCameraFramesWorker_2.ImageUpdated.connect(lambda image: self.ShowCamera2(image))

        # Start the worker thread
        self.CaptureIpCameraFramesWorker_2.start()

        self.CaptureIpCameraFramesWorker_3 = CaptureIpCameraFramesWorker(url=self.url_3, output_filename='Section_C_Recording', camera_name='Section C')

        # Connect the signal from worker to the slot method
        self.CaptureIpCameraFramesWorker_3.ImageUpdated.connect(lambda image: self.ShowCamera3(image))

        # Start the worker thread
        self.CaptureIpCameraFramesWorker_3.start()

        

       
        # # Start the thread getIpCameraFrameWorker_1.
        # self.CaptureIpCameraFramesWorker_1.start()

       

        # # Start the thread getIpCameraFrameWorker_2.
        # self.CaptureIpCameraFramesWorker_2.start()

        

        # # Start the thread getIpCameraFrameWorker_3.
        # self.CaptureIpCameraFramesWorker_3.start()

        

        # # Start the thread getIpCameraFrameWorker_4.
        # self.CaptureIpCameraFramesWorker_4.start()


        self.original_root_index = self.tree_view.rootIndex()

    @pyqtSlot()
    def ShowCamera11(self, frame: QImage) -> None:
        # Perform face recognition for Camera_1 using FaceManager
        faces = self.face_manager.recognize_faces_for_camera("Section A", frame)
        print(f"Detected faces for Camera_1: {faces}")

        self.camera_1.setPixmap(QPixmap.fromImage(frame))  

    @pyqtSlot()
    def ShowCamera12(self, frame: QImage) -> None:
        # Perform face recognition for Camera_1 using FaceManager
        faces = self.face_manager.recognize_faces_for_camera("Section B", frame)
        print(f"Detected faces for Camera_1: {faces}")

        self.camera_1.setPixmap(QPixmap.fromImage(frame))

    
    def __SetupUI(self) -> None:
        """Set up the User Interface."""

        # Add widgets to layout.
          # Create a QSplitter for the main window
        # self.play_back_widget = QStackedWidget()
        self.main_splitter = QSplitter(Qt.Horizontal) #type:ignore
        self.vbox = QVBoxLayout()

        self.search_container = QWidget()
        layout = QHBoxLayout(self.search_container)

        self.frame = QFrame()
        self.frame.resize(300,300)
        frame_layout = QVBoxLayout(self.frame)


        # Create a QSplitter for the left side (video list and player)
        left_splitter = QSplitter(Qt.Vertical) #type:ignore
        right_splitter = QSplitter(Qt.Horizontal) #type:ignore


        self.video_widgets = []
        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setSortingEnabled(True)

        

        # Create a stacked widget to hold video players
        self.stacked_video_players = QStackedWidget()

        # Select the parent folder containing subfolders with video files
        parent_folder = r"C:/Users/PC/Desktop/v0.11/recordings"

        # Create a file system model
        # model = QFileSystemModel()
        self.model = QFileSystemModel()
        self.model.setRootPath(parent_folder)
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files )
        # Set the model for the tree view
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(parent_folder))
        
        self.tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setSortingEnabled(True)

        frame_layout.addWidget(self.search_container)

        # Set the size policy of the QFrame containing the QTreeView
        self.frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        frame_layout.addWidget(self.tree_view)

        # Automatically resize columns based on content
        self.tree_view.header().setSectionResizeMode(QHeaderView.ResizeToContents) #type: ignore
        frame_layout.addWidget(self.tree_view)
        
        # Handle item selection in the tree view
        self.tree_view.clicked.connect(self.treeItemClicked)

        self.folder_input = QLineEdit(self)
        self.folder_input.setPlaceholderText("Enter Location name...")
        self.folder_input.returnPressed.connect(self.set_current_folder)

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search files Name of a Person...")
        self.search_box.textChanged.connect(self.filter_files)
       

        
        layout.addWidget(self.folder_input)
        layout.addWidget(self.search_box)
        


        
        self.detect_button = QPushButton("On/Off")
        self.detect_button.clicked.connect(self.toggle_face_detection)
        layout.addWidget(self.detect_button)

        self.url_frame = QFrame()
        # self.url_frame.resize(5,5)
        self.url_frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.url_frame.setMaximumHeight(300)
        self.url_frame_layout = QVBoxLayout(self.url_frame)

        self.url1_setup = QLineEdit(self)
        self.url1_setup.setPlaceholderText("Enter RTSP URL for camera 1")
        self.url_frame_layout.addWidget(self.url1_setup)
        self.url1_setup.returnPressed.connect(self.set_current_folder)

        self.url2_setup = QLineEdit(self)
        self.url2_setup.setPlaceholderText("Enter RTSP URL for camera 2")
        self.url_frame_layout.addWidget(self.url2_setup)
        self.url2_setup.returnPressed.connect(self.set_current_folder)

        self.url3_setup = QLineEdit(self)
        self.url3_setup.setPlaceholderText("Enter RTSP URL for camera 3")
        self.url_frame_layout.addWidget(self.url3_setup)
        self.url3_setup.returnPressed.connect(self.set_current_folder)

        self.url4_setup = QLineEdit(self)
        self.url4_setup.setPlaceholderText("Enter RTSP URL for camera 4")
        self.url_frame_layout.addWidget(self.url4_setup)
        self.url4_setup.returnPressed.connect(self.set_current_folder)

        self.url_button = QPushButton()
        self.url_button.setText("Set URLs")
        
        self.url_button.resize(150, 50)
        self.url_frame_layout.addWidget(self.url_button)
       
       
        left_splitter.addWidget(self.url_frame) 
        left_splitter.addWidget(self.frame)
        left_splitter.addWidget(self.stacked_video_players)
        


        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # file_path1 = "C:/Users/PC/Desktop/v0.10/ipcamerarecordings/Section A"
        # file_path2 = "C:/Users/PC/Desktop/v0.10/ipcamerarecordings/Section A"
        # file_path3 = "C:/Users/PC/Desktop/v0.10/ipcamerarecordings/Section A"
        # file_path4 = "C:/Users/PC/Desktop/v0.10/ipcamerarecordings/Section A"

        # # Worker2(file_path1, '.mp4', self)

        # self.video_player1 = VideoPlayer(file_path1)
        # self.video_player2 = VideoPlayer(file_path2)
        # self.video_player3 = VideoPlayer(file_path3)
        # self.video_player4 = VideoPlayer(file_path4)

        
        
        # Add a playback speed slider for each camera below the camera
        # self.playback_speed_slider_1 = QSlider(Qt.Horizontal)
        # self.playback_speed_slider_1.setFixedHeight(15)  # Adjust the height as needed
        grid_layout.addWidget(self.QScrollArea_1, 0, 0)
        # grid_layout.addWidget(self.video_player1, 0, 0)
        # grid_layout.addWidget(self.playback_speed_slider_1, 1, 0)

        # self.playback_speed_slider_2 = QSlider(Qt.Horizontal)
        # self.playback_speed_slider_2.setFixedHeight(15)
        grid_layout.addWidget(self.QScrollArea_2, 0, 1)
        # grid_layout.addWidget(self.video_player2, 0, 1)
        # grid_layout.addWidget(self.playback_speed_slider_2, 1, 1)

        # self.playback_speed_slider_3 = QSlider(Qt.Horizontal)
        # self.playback_speed_slider_3.setFixedHeight(15)
        grid_layout.addWidget(self.QScrollArea_3, 2, 0)
        # grid_layout.addWidget(self.video_player3, 2, 0)
        # grid_layout.addWidget(self.playback_speed_slider_3, 3, 0)

        # self.playback_speed_slider_4 = QSlider(Qt.Horizontal)
        # self.playback_speed_slider_4.setFixedHeight(15)
        grid_layout.addWidget(self.QScrollArea_4, 2, 1)
        # grid_layout.addWidget(self.video_player4, 2, 1)
        # grid_layout.addWidget(self.playback_speed_slider_4, 3, 1)

        # self.clicked = CaptureIpCameraFramesWorker.face_button_clicked
        # self.detect_button = QPushButton("Detect Faces")
        # self.detect_button.clicked.connect(self.clicked)
        # grid_layout.addWidget(self.detect_button, 4, 0, 1, 2)     

        # Create a widget instance.
        self.widget = QWidget(self)
        self.widget.setLayout(grid_layout)
        right_splitter.addWidget(self.widget)

        

        self.main_splitter.addWidget(left_splitter)
        self.main_splitter.addWidget(right_splitter)
        self.main_splitter.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        
        
        # Set the central widget.
        self.setCentralWidget(self.main_splitter)
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setStyleSheet("QMainWindow {background: 'white';}")
        self.setWindowIcon(QIcon(QPixmap("./logo/allSeingEye.png")))
        # Set window title.
        self.setWindowTitle("OmniVisionAI")



   
    
    def set_current_folder(self):
        folder_name = self.folder_input.text()
        root_index = self.tree_view.rootIndex()

        if not folder_name:
            # Reset to the original path directory
            self.tree_view.setRootIndex(self.original_root_index)
            self.filter_files()
            return

        for row in range(self.model.rowCount(root_index)):
            child_index = self.model.index(row, 0, root_index)
            child_name = self.model.fileName(child_index).lower()

            if folder_name.lower() in child_name and self.model.isDir(child_index):
                self.tree_view.setRootIndex(child_index)
                self.filter_files()
                return

    def filter_files(self):
        search_text = self.search_box.text().lower()
        root_index = self.tree_view.rootIndex()
        self.filter_recursive(root_index, search_text)

    def filter_recursive(self, parent_index, search_text):
        for row in range(self.model.rowCount(parent_index)):
            child_index = self.model.index(row, 0, parent_index)
            file_name = self.model.fileName(child_index).lower()

            if search_text in file_name:
                # Show the item
                self.tree_view.setRowHidden(row, parent_index, False)
            else:
                # Hide the item
                self.tree_view.setRowHidden(row, parent_index, True)

            # Recursively search in subfolders
            if self.model.isDir(child_index):
                self.filter_recursive(child_index, search_text)   

    def toggle_face_detection(self):
        # Toggle the face_clicked flag for all workers
        for worker in [
        self.CaptureIpCameraFramesWorker_1,
        self.CaptureIpCameraFramesWorker_2,
        self.CaptureIpCameraFramesWorker_3,
        # self.CaptureIpCameraFramesWorker_4,
        ]:
         worker.face_clicked = not worker.face_clicked

        
    def treeItemClicked(self, index):
        file_info = self.tree_view.model().fileInfo(index) #type: ignore

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

    @QtCore.pyqtSlot()
    def ShowCamera1(self, frame: QImage) -> None:
         self.camera_1.setPixmap(QPixmap.fromImage(frame))
        # self.video_player1.show_frame(frame)


    @QtCore.pyqtSlot()
    def ShowCamera2(self, frame: QImage) -> None:
        self.camera_2.setPixmap(QPixmap.fromImage(frame))
        # self.video_player2.show_frame(frame)

    @QtCore.pyqtSlot()
    def ShowCamera3(self, frame: QImage) -> None:
        self.camera_3.setPixmap(QPixmap.fromImage(frame))
        # self.video_player3.show_frame(frame)

    @QtCore.pyqtSlot()
    def ShowCamera4(self, frame: QImage) -> None:
        self.camera_4.setPixmap(QPixmap.fromImage(frame))
        # self.video_player4.show_frame(QPixmap.fromImage(frame))

    

    # Override method for class MainWindow.
    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """
        Method to capture the events for objects with an event filter installed.
        :param source: The object for whom an event took place.
        :param event: The event that took place.
        :return: True if event is handled.
        """
        #
        if event.type() == QtCore.QEvent.MouseButtonDblClick: #type: ignore
            if source.objectName() == 'Camera_1':
                #
                if self.list_of_cameras_state["Camera_1"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    # self.playback_speed_slider_2.hide()
                    # self.playback_speed_slider_3.hide()
                    # self.playback_speed_slider_4.hide()
                    # self.video_player2.hide()
                    # self.video_player3.hide()
                    # self.video_player4.hide()
                    self.list_of_cameras_state["Camera_1"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    # self.playback_speed_slider_2.show()
                    # self.playback_speed_slider_3.show()
                    # self.playback_speed_slider_4.show()
                    # self.video_player2.show()
                    # self.video_player3.show()
                    # self.video_player4.show()
                    self.list_of_cameras_state["Camera_1"] = "Normal"
            elif source.objectName() == 'Camera_2':
                #
                if self.list_of_cameras_state["Camera_2"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    # self.playback_speed_slider_1.hide()
                    # self.playback_speed_slider_3.hide()
                    # self.playback_speed_slider_4.hide()
                    # self.video_player1.hide()
                    # self.video_player3.hide()
                    # self.video_player4.hide()
                    self.list_of_cameras_state["Camera_2"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    # self.playback_speed_slider_1.show()
                    # self.playback_speed_slider_3.show()
                    # self.playback_speed_slider_4.show()
                    # self.video_player1.show()
                    # self.video_player3.show()
                    # self.video_player4.show()
                    self.list_of_cameras_state["Camera_2"] = "Normal"
            elif source.objectName() == 'Camera_3':
                #
                if self.list_of_cameras_state["Camera_3"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_4.hide()
                    # self.playback_speed_slider_1.hide()
                    # self.playback_speed_slider_2.hide()
                    # self.playback_speed_slider_4.hide()
                    # self.video_player1.hide()
                    # self.video_player2.hide()
                    # self.video_player4.hide()
                    self.list_of_cameras_state["Camera_3"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_4.show()
                    # self.playback_speed_slider_1.show()
                    # self.playback_speed_slider_2.show()
                    # self.playback_speed_slider_4.show()
                    # self.video_player1.show()
                    # self.video_player2.show()
                    # self.video_player4.show()
                    self.list_of_cameras_state["Camera_3"] = "Normal"
            elif source.objectName() == 'Camera_4':
                #
                if self.list_of_cameras_state["Camera_4"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    # self.playback_speed_slider_1.hide()
                    # self.playback_speed_slider_2.hide()
                    # self.playback_speed_slider_3.hide()
                    # self.video_player1.hide()
                    # self.video_player2.hide()
                    # self.video_player3.hide()
                    self.list_of_cameras_state["Camera_4"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    # self.playback_speed_slider_1.show()
                    # self.playback_speed_slider_2.show()
                    # self.playback_speed_slider_3.show()
                    # self.video_player1.show()
                    # self.video_player2.show()
                    # self.video_player3.show()
                    self.list_of_cameras_state["Camera_4"] = "Normal"
            else:
                return super(MainWindow, self).eventFilter(source, event)
            return True
        else:
            return super(MainWindow, self).eventFilter(source, event)

    # Overwrite method closeEvent from class QMainWindow.
    def closeEvent(self, event) -> None:
        # If thread getIpCameraFrameWorker_1 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_1.isRunning():
            self.CaptureIpCameraFramesWorker_1.quit()
        # If thread getIpCameraFrameWorker_2 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_2.isRunning():
            self.CaptureIpCameraFramesWorker_2.quit()
        # If thread getIpCameraFrameWorker_3 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_3.isRunning():
            self.CaptureIpCameraFramesWorker_3.quit()
        # Accept the event
        event.accept()



def main() -> None:
    # Create a QApplication object. It manages the GUI application's control flow and main settings.
    # It handles widget specific initialization, finalization.
    # For any GUI application using Qt, there is precisely one QApplication object
    app = QApplication(sys.argv)

    # widget = QStackedWidget()

    
    # Create an instance of the class MainWindow.
    window = MainWindow()

    # playback= Play_Back_Screen()
    
    # widget.addWidget(window)
    # widget.addWidget(playback)

    # Show the window.
    window.show()
    # Start Qt event loop.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
