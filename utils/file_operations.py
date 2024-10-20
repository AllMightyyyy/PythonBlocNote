# utils/file_operations.py

import os
from PySide6.QtWidgets import QFileDialog

def open_file_dialog(parent, file_filter="All Files (*.*)"):
    file_path, _ = QFileDialog.getOpenFileName(parent, "Open File", os.getenv('HOME'), file_filter)
    return file_path

def save_file_dialog(parent, file_filter="All Files (*.*)"):
    file_path, _ = QFileDialog.getSaveFileName(parent, "Save File", os.getenv('HOME'), file_filter)
    return file_path
