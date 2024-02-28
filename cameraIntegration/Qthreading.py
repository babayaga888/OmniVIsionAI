import sys
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
import cv2

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)

        self.Worker1 = Worker1()

        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True

        # Find the first available webcam
        camera_index = None
        for i in range(10):  # Try up to 10 camera indices
            capture = cv2.VideoCapture(i)
            if capture.isOpened():
                camera_index = i
                break

        if camera_index is None:
            # No available webcams found
            self.ImageUpdate.emit(QImage())  # Emit an empty image
            self.ThreadActive = False
            return

        capture = cv2.VideoCapture(camera_index)

        while self.ThreadActive:
            ret, frame = capture.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            flipped_image = cv2.flip(image, 1)
            qt_image = QImage(
                flipped_image.data,
                flipped_image.shape[1],
                flipped_image.shape[0],
                QImage.Format_RGB888,
            )
            pic = qt_image.scaled(640, 480, Qt.KeepAspectRatio) # type: ignore

            self.ImageUpdate.emit(pic)

        capture.release()

    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())