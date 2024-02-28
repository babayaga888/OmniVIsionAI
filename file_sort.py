from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout

# class FileSearchWidget(QWidget):
#     def __init__(self):
#         super(FileSearchWidget, self).__init__()

#         initial_folder_path = r"C:\Users\PC\Desktop\v0.10\recordings"

#         self.model = QFileSystemModel()
#         self.model.setRootPath(initial_folder_path)

#         self.tree_view = QTreeView()
#         self.tree_view.setModel(self.model)
#         self.tree_view.setRootIndex(self.model.index(initial_folder_path))

#         self.folder_input = QLineEdit(self)
#         self.folder_input.setPlaceholderText("Enter folder name...")
#         self.folder_input.returnPressed.connect(self.set_current_folder)

#         self.search_box = QLineEdit(self)
#         self.search_box.setPlaceholderText("Search files and folders...")
#         self.search_box.textChanged.connect(self.filter_files)

#         layout = QVBoxLayout()
#         input_layout = QHBoxLayout()
#         input_layout.addWidget(self.folder_input)
#         input_layout.addWidget(self.search_box)
#         layout.addLayout(input_layout)
#         layout.addWidget(self.tree_view)
#         self.setLayout(layout)

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