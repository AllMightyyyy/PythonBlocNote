# widgets/status_bar.py

from PySide6.QtWidgets import QStatusBar, QLabel

class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.message_label = QLabel()
        self.word_count_label = QLabel("Words: 0")
        self.addPermanentWidget(self.word_count_label)
        self.show_message("Ready")

    def show_message(self, message, timeout=5000):
        self.message_label.setText(message)
        self.showMessage(message, timeout)

    def update_word_count(self, count):
        self.word_count_label.setText(f"Words: {count}")
