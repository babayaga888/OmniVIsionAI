# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
#     QLabel, QGridLayout, QScrollArea, QSizePolicy
# from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette
# from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent, QObject, QSize
# from PyQt5 import QtCore


# import sys
# from PyQt5.QtCore import Qt, QUrl
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# from PyQt5.QtMultimediaWidgets import QVideoWidget

# import sys
# from PyQt5.QtCore import Qt, QUrl
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
# from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# from PyQt5.QtMultimediaWidgets import QVideoWidget

# class RTSPPlayer(QMainWindow):
#     def __init__(self, rtsp_url):
#         super(RTSPPlayer, self).__init__()

#         self.setWindowTitle("RTSP Player")
#         self.setGeometry(100, 100, 800, 600)

#         # Create QMediaPlayer and set the RTSP stream
#         self.media_player = QMediaPlayer(self)
#         self.media_player.setMedia(QMediaContent(QUrl(rtsp_url)))

#         # Create QVideoWidget to display the video
#         self.video_widget = QVideoWidget(self)
#         self.media_player.setVideoOutput(self.video_widget)

#         # Create QSlider for playback control
#         self.playback_slider = QSlider(Qt.Horizontal)
#         self.playback_slider.setRange(0, 100)
#         self.playback_slider.sliderMoved.connect(self.setPlaybackPosition)
#         self.media_player.positionChanged.connect(self.updateSlider)

#         # Create layout and set central widget
#         layout = QVBoxLayout()
#         layout.addWidget(self.video_widget)
#         layout.addWidget(self.playback_slider)

#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#         # Play the RTSP stream
#         self.media_player.play()

#     def setPlaybackPosition(self, position):
#         duration = self.media_player.duration()
#         self.media_player.setPosition(int(position * duration / 100))

#     def updateSlider(self, position):
#         duration = self.media_player.duration()
#         if duration > 0:
#             progress = int(position * 100 / duration)
#             self.playback_slider.setValue(progress)

# def main():
#     app = QApplication(sys.argv)

#     # Replace 'rtsp://your_rtsp_stream_url' with the actual RTSP stream URL
#     rtsp_url = 'rtsp://admin:hesoyam213@192.168.1.108:554/cam/playback?channel=1&subtype=0'
#     player = RTSPPlayer(rtsp_url)
#     player.show()

#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()

    
# from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
#         QTime)
# from PyQt5.QtGui import QStandardItemModel
# from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
#         QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView,
#         QVBoxLayout, QWidget)


# class MySortFilterProxyModel(QSortFilterProxyModel):
#     def __init__(self, parent=None):
#         super(MySortFilterProxyModel, self).__init__(parent)

#         self.minDate = QDate()
#         self.maxDate = QDate()

#     def setFilterMinimumDate(self, date):
#         self.minDate = date
#         self.invalidateFilter()

#     def filterMinimumDate(self):
#         return self.minDate

#     def setFilterMaximumDate(self, date):
#         self.maxDate = date
#         self.invalidateFilter()
 
#     def filterMaximumDate(self):
#         return self.maxDate

#     def filterAcceptsRow(self, sourceRow, sourceParent):
#         index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
#         index1 = self.sourceModel().index(sourceRow, 1, sourceParent)
#         index2 = self.sourceModel().index(sourceRow, 2, sourceParent)

#         return (   (self.filterRegExp().indexIn(self.sourceModel().data(index0)) >= 0
#                     or self.filterRegExp().indexIn(self.sourceModel().data(index1)) >= 0)
#                 and self.dateInRange(self.sourceModel().data(index2)))

#     def lessThan(self, left, right):
#         leftData = self.sourceModel().data(left)
#         rightData = self.sourceModel().data(right)

#         if not isinstance(leftData, QDate):
#             emailPattern = QRegExp("([\\w\\.]*@[\\w\\.]*)")

#             if left.column() == 1 and emailPattern.indexIn(leftData) != -1:
#                 leftData = emailPattern.cap(1)

#             if right.column() == 1 and emailPattern.indexIn(rightData) != -1:
#                 rightData = emailPattern.cap(1)

#         return leftData < rightData

#     def dateInRange(self, date):
#         if isinstance(date, QDateTime):
#             date = date.date()

#         return (    (not self.minDate.isValid() or date >= self.minDate)
#                 and (not self.maxDate.isValid() or date <= self.maxDate))


# class Window(QWidget):
#     def __init__(self):
#         super(Window, self).__init__()

#         self.proxyModel = MySortFilterProxyModel(self)
#         self.proxyModel.setDynamicSortFilter(True)

#         self.sourceView = QTreeView()
#         self.sourceView.setRootIsDecorated(False)
#         self.sourceView.setAlternatingRowColors(True)

#         sourceLayout = QHBoxLayout()
#         sourceLayout.addWidget(self.sourceView)
#         sourceGroupBox = QGroupBox("Original Model")
#         sourceGroupBox.setLayout(sourceLayout)

#         self.filterCaseSensitivityCheckBox = QCheckBox("Case sensitive filter")
#         self.filterCaseSensitivityCheckBox.setChecked(True)
#         self.filterPatternLineEdit = QLineEdit()
#         self.filterPatternLineEdit.setText("Grace|Sports")
#         filterPatternLabel = QLabel("&Filter pattern:")
#         filterPatternLabel.setBuddy(self.filterPatternLineEdit)
#         self.filterSyntaxComboBox = QComboBox()
#         self.filterSyntaxComboBox.addItem("Regular expression", QRegExp.RegExp)
#         self.filterSyntaxComboBox.addItem("Wildcard", QRegExp.Wildcard)
#         self.filterSyntaxComboBox.addItem("Fixed string", QRegExp.FixedString)
#         self.fromDateEdit = QDateEdit()
#         self.fromDateEdit.setDate(QDate(2006, 12, 22))
#         self.fromDateEdit.setCalendarPopup(True)
#         fromLabel = QLabel("F&rom:")
#         fromLabel.setBuddy(self.fromDateEdit)
#         self.toDateEdit = QDateEdit()
#         self.toDateEdit.setDate(QDate(2007, 1, 5))
#         self.toDateEdit.setCalendarPopup(True)
#         toLabel = QLabel("&To:")
#         toLabel.setBuddy(self.toDateEdit)

#         self.filterPatternLineEdit.textChanged.connect(self.textFilterChanged)
#         self.filterSyntaxComboBox.currentIndexChanged.connect(self.textFilterChanged)
#         self.filterCaseSensitivityCheckBox.toggled.connect(self.textFilterChanged)
#         self.fromDateEdit.dateChanged.connect(self.dateFilterChanged)
#         self.toDateEdit.dateChanged.connect(self.dateFilterChanged)

#         self.proxyView = QTreeView()
#         self.proxyView.setRootIsDecorated(False)
#         self.proxyView.setAlternatingRowColors(True)
#         self.proxyView.setModel(self.proxyModel)
#         self.proxyView.setSortingEnabled(True)
#         self.proxyView.sortByColumn(1, Qt.AscendingOrder)

#         self.textFilterChanged()
#         self.dateFilterChanged()

#         proxyLayout = QGridLayout()
#         proxyLayout.addWidget(self.proxyView, 0, 0, 1, 3)
#         proxyLayout.addWidget(filterPatternLabel, 1, 0)
#         proxyLayout.addWidget(self.filterPatternLineEdit, 1, 1)
#         proxyLayout.addWidget(self.filterSyntaxComboBox, 1, 2)
#         proxyLayout.addWidget(self.filterCaseSensitivityCheckBox, 2, 0, 1, 3)
#         proxyLayout.addWidget(fromLabel, 3, 0)
#         proxyLayout.addWidget(self.fromDateEdit, 3, 1, 1, 2)
#         proxyLayout.addWidget(toLabel, 4, 0)
#         proxyLayout.addWidget(self.toDateEdit, 4, 1, 1, 2)
#         proxyGroupBox = QGroupBox("Sorted/Filtered Model")
#         proxyGroupBox.setLayout(proxyLayout)

#         mainLayout = QVBoxLayout()
#         mainLayout.addWidget(sourceGroupBox)
#         mainLayout.addWidget(proxyGroupBox)
#         self.setLayout(mainLayout)

#         self.setWindowTitle("Custom Sort/Filter Model")
#         self.resize(500, 450)

#     def setSourceModel(self, model):
#         self.proxyModel.setSourceModel(model)
#         self.sourceView.setModel(model)

#     def textFilterChanged(self):
#         syntax = QRegExp.PatternSyntax(
#             self.filterSyntaxComboBox.itemData(
#                 self.filterSyntaxComboBox.currentIndex()))
#         caseSensitivity = (
#             self.filterCaseSensitivityCheckBox.isChecked()
#             and Qt.CaseSensitive or Qt.CaseInsensitive)
#         regExp = QRegExp(self.filterPatternLineEdit.text(), caseSensitivity, syntax)
#         self.proxyModel.setFilterRegExp(regExp)

#     def dateFilterChanged(self):
#         self.proxyModel.setFilterMinimumDate(self.fromDateEdit.date())
#         self.proxyModel.setFilterMaximumDate(self.toDateEdit.date())


# def addMail(model, subject, sender, date):
#     model.insertRow(0)
#     model.setData(model.index(0, 0), subject)
#     model.setData(model.index(0, 1), sender)
#     model.setData(model.index(0, 2), date)


# def createMailModel(parent):
#     model = QStandardItemModel(0, 3, parent)

#     model.setHeaderData(0, Qt.Horizontal, "Subject")
#     model.setHeaderData(1, Qt.Horizontal, "Sender")
#     model.setHeaderData(2, Qt.Horizontal, "Date")

#     addMail(model, "Happy New Year!", "Grace K. <grace@software-inc.com>",
#             QDateTime(QDate(2006, 12, 31), QTime(17, 3)))
#     addMail(model, "Radically new concept", "Grace K. <grace@software-inc.com>",
#             QDateTime(QDate(2006, 12, 22), QTime(9, 44)))
#     addMail(model, "Accounts", "pascale@nospam.com",
#             QDateTime(QDate(2006, 12, 31), QTime(12, 50)))
#     addMail(model, "Expenses", "Joe Bloggs <joe@bloggs.com>",
#             QDateTime(QDate(2006, 12, 25), QTime(11, 39)))
#     addMail(model, "Re: Expenses", "Andy <andy@nospam.com>",
#             QDateTime(QDate(2007, 1, 2), QTime(16, 5)))
#     addMail(model, "Re: Accounts", "Joe Bloggs <joe@bloggs.com>",
#             QDateTime(QDate(2007, 1, 3), QTime(14, 18)))
#     addMail(model, "Re: Accounts", "Andy <andy@nospam.com>",
#             QDateTime(QDate(2007, 1, 3), QTime(14, 26)))
#     addMail(model, "Sports", "Linda Smith <linda.smith@nospam.com>",
#             QDateTime(QDate(2007, 1, 5), QTime(11, 33)))
#     addMail(model, "AW: Sports", "Rolf Newschweinstein <rolfn@nospam.com>",
#             QDateTime(QDate(2007, 1, 5), QTime(12, 0)))
#     addMail(model, "RE: Sports", "Petra Schmidt <petras@nospam.com>",
#             QDateTime(QDate(2007, 1, 5), QTime(12, 1)))

#     return model


# if __name__ == "__main__":

#     import sys

#     app = QApplication(sys.argv)

#     window = Window()
#     window.setSourceModel(createMailModel(window))
#     window.show()

#     sys.exit(app.exec_())

from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout

class FileSearchWidget(QWidget):
    def __init__(self):
        super(FileSearchWidget, self).__init__()

        initial_folder_path = r"C:\Users\PC\Desktop\v0.10\recordings"

        self.model = QFileSystemModel()
        self.model.setRootPath(initial_folder_path)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(initial_folder_path))

        self.folder_input = QLineEdit(self)
        self.folder_input.setPlaceholderText("Enter folder name...")
        self.folder_input.returnPressed.connect(self.set_current_folder)

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search files and folders...")
        self.search_box.textChanged.connect(self.filter_files)

        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.folder_input)
        input_layout.addWidget(self.search_box)
        layout.addLayout(input_layout)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

    def set_current_folder(self):
        folder_name = self.folder_input.text()
        root_index = self.tree_view.rootIndex()

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


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)

    window = FileSearchWidget()
    window.show()

    sys.exit(app.exec_())