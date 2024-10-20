from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox
)
from PySide6.QtCore import Qt

class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")
        self.setModal(True)  
        self.setup_ui()
        self.parent = parent

    def setup_ui(self):
        # Labels and LineEdits
        find_label = QLabel("Find:")
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Enter text to find")  

        replace_label = QLabel("Replace:")
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Enter replacement text")  

        # Buttons
        self.find_button = QPushButton("Find Next")
        self.replace_button = QPushButton("Replace")
        self.replace_all_button = QPushButton("Replace All")
        self.close_button = QPushButton("Close")

        # Layouts
        find_layout = QHBoxLayout()
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_input)

        replace_layout = QHBoxLayout()
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.find_button)
        buttons_layout.addWidget(self.replace_button)
        buttons_layout.addWidget(self.replace_all_button)
        buttons_layout.addWidget(self.close_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(find_layout)
        main_layout.addLayout(replace_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        # Connect buttons
        self.find_button.clicked.connect(self.find_next)
        self.replace_button.clicked.connect(self.replace)
        self.replace_all_button.clicked.connect(self.replace_all)
        self.close_button.clicked.connect(self.close)

    def find_next(self):
        text = self.find_input.text()
        if not text:
            QMessageBox.warning(self, "Input Required", "Please enter text to find.")  
            return
        self.parent.find_text(text)  

    def replace(self):
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        if not find_text:
            QMessageBox.warning(self, "Input Required", "Please enter text to find.")
            return
        self.parent.replace_text(find_text, replace_text)

    def replace_all(self):
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        if not find_text:
            QMessageBox.warning(self, "Input Required", "Please enter text to find.")
            return
        self.parent.replace_all_text(find_text, replace_text)

    def showEvent(self, event):
        super().showEvent(event)
        self.find_input.setFocus()  
