import sys
import os
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QColorDialog,
    QFontDialog,
    QInputDialog,
    QStyle,
)
from PySide6.QtGui import QIcon, QTextListFormat, QFont
from PySide6.QtCore import Qt

from widgets.editor import Editor
from widgets.menu_bar import MenuBar
from widgets.tool_bar import ToolBar
from widgets.status_bar import StatusBar
from widgets.find_replace_dialog import FindReplaceDialog
from utils.file_operations import open_file_dialog, save_file_dialog
from utils.helpers import count_words

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note Editor")
        icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'icons', 'save.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.resize(800, 600)

        self.current_file = None

        self.init_ui()

    def init_ui(self):

        self.editor = Editor(self)
        self.setCentralWidget(self.editor)

        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)

        self.find_replace_dialog = FindReplaceDialog(self)

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.tool_bar = ToolBar(self)
        self.addToolBar(self.tool_bar)

        self.apply_theme("light") # DEFAULT THEME HERE

        self.init_autosave()

    def new_file(self):
        if self.maybe_save():
            self.editor.clear()
            self.current_file = None
            self.status_bar.show_message("New file created.")

    def open_file(self):
        if self.maybe_save():
            file_path = open_file_dialog(
                self,
                "Text Files (*.txt);;Markdown Files (*.md);;Rich Text Files (*.rtf);;All Files (*.*)"
            )
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.editor.setPlainText(content)
                    self.current_file = file_path
                    self.status_bar.show_message(f"Opened '{os.path.basename(file_path)}'")
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not open file: {e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.editor.toPlainText())
                self.status_bar.show_message("File saved successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save file: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = save_file_dialog(
            self,
            "Text Files (*.txt);;Markdown Files (*.md);;Rich Text Files (*.rtf);;All Files (*.*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.editor.toPlainText())
                self.current_file = file_path
                self.status_bar.show_message("File saved successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save file: {e}")

    def export_as_pdf(self):
        QMessageBox.information(self, "Export", "Export as PDF is not implemented yet.") # FIND LIBRARY FOR TEXT TO PDF

    def maybe_save(self):
        if self.editor.document().isModified():
            ret = QMessageBox.warning(
                self,
                "Unsaved Changes",
                "The document has been modified.\nDo you want to save your changes?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
            )
            if ret == QMessageBox.StandardButton.Save:
                self.save_file()
                return True
            elif ret == QMessageBox.StandardButton.Discard:
                return True
            else:
                return False
        return True

    def toggle_toolbar(self, state):
        self.tool_bar.setVisible(state)

    def toggle_statusbar(self, state):
        self.status_bar.setVisible(state)

    def zoom_in(self):
        current_font = self.editor.font()
        current_size = current_font.pointSize()
        current_font.setPointSize(current_size + 1)
        self.editor.setFont(current_font)
        self.status_bar.show_message(f"Zoomed In to {current_font.pointSize()}pt.")

    def zoom_out(self):
        current_font = self.editor.font()
        current_size = current_font.pointSize()
        if current_size > 6:  # WE DONT WANT FONT SIZE SMALL
            current_font.setPointSize(current_size - 1)
            self.editor.setFont(current_font)
            self.status_bar.show_message(f"Zoomed Out to {current_font.pointSize()}pt.")

    def reset_zoom(self):
        default_font = QFont("Segoe UI", 12)
        self.editor.setFont(default_font)
        self.status_bar.show_message("Zoom reset to default (12pt).")

    def find_text(self, text):
        if not text:
            QMessageBox.warning(self, "Input Required", "Please enter text to find.")
            return

        cursor = self.editor.textCursor()
        document = self.editor.document()

        if cursor.hasSelection():
            search_start = cursor.selectionEnd()
        else:
            search_start = cursor.position()

        found_cursor = document.find(text, search_start)

        if found_cursor.isNull():
            found_cursor = document.find(text, 0)

        if not found_cursor.isNull():
            self.editor.setTextCursor(found_cursor)
            self.editor.setFocus()
            self.status_bar.show_message(f"Found '{text}'.")
        else:
            QMessageBox.information(self, "Find", f"'{text}' not found.")
            self.status_bar.show_message(f"'{text}' not found.")


    def replace_text(self, find_text, replace_text):
        if not find_text:
            return
        
        cursor = self.editor.textCursor()

        if cursor.hasSelection() and cursor.selectedText() == find_text:
            cursor.insertText(replace_text)
            self.status_bar.show_message(f"Replaced '{find_text}' with '{replace_text}'.")
            self.find_text(find_text)
        else:
            self.find_text(find_text)

    def replace_all_text(self, find_text, replace_text):
        if not find_text:
            return

        document = self.editor.document()
        cursor = self.editor.textCursor()
        cursor.beginEditBlock() 

        found_cursor = document.find(find_text, 0) 
        occurrences = 0

        while not found_cursor.isNull():
            occurrences += 1
            found_cursor.insertText(replace_text)
            found_cursor = document.find(find_text, found_cursor)

        cursor.endEditBlock()

        if occurrences > 0:
            self.status_bar.show_message(f"Replaced all {occurrences} occurrences of '{find_text}' with '{replace_text}'.")
        else:
            self.status_bar.show_message(f"No occurrences of '{find_text}' found.")

    def change_font(self):
        font, ok = QFontDialog.getFont(self.editor.font(), self, "Select Font")
        if ok and isinstance(font, QFont):
            self.editor.setFont(font)
            self.status_bar.show_message(f"Font changed to {font.family()}, {font.pointSize()}pt.")
        else:
            self.status_bar.show_message("Font change canceled or invalid font selected.")

    def change_text_color(self):
        color = QColorDialog.getColor(self.editor.textColor(), self, "Select Text Color")
        if color.isValid():
            self.editor.setTextColor(color)
            self.status_bar.show_message(f"Text color changed to {color.name()}.")

    def change_bg_color(self):
        color = QColorDialog.getColor(
            self.editor.palette().color(self.editor.backgroundRole()),
            self,
            "Select Background Color"
        )
        if color.isValid():
            self.editor.setStyleSheet(f"background-color: {color.name()};")
            self.status_bar.show_message(f"Background color changed to {color.name()}.")

    def add_bullets(self):
        cursor = self.editor.textCursor()
        cursor.insertList(QTextListFormat.ListDisc)
        self.status_bar.show_message("Bulleted list added.")

    def add_numbering(self):
        cursor = self.editor.textCursor()
        cursor.insertList(QTextListFormat.ListDecimal)
        self.status_bar.show_message("Numbered list added.")

    # Tools
    def show_word_count(self):
        count = self.editor.word_count
        QMessageBox.information(self, "Word Count", f"Total Words: {count}")

    def spell_check(self):
        self.editor.highlighter.rehighlight()
        self.status_bar.show_message("Spell check completed.")

    def open_thesaurus(self):
        QMessageBox.information(self, "Thesaurus", "Thesaurus is not implemented yet.")

    def select_language(self):
        languages = ["English", "Spanish", "French", "German", "Chinese"]
        language, ok = QInputDialog.getItem(self, "Select Language", "Language:", languages, 0, False)
        if ok and language:
            QMessageBox.information(self, "Language Selection", f"Language set to {language}.")

    # Help
    def open_documentation(self):
        QMessageBox.information(self, "Documentation", "Documentation is not available yet.")

    def show_about(self):
        QMessageBox.information(
            self,
            "About Note Editor",
            "Copyright reserved for zakaria."
        )

    def check_updates(self):
        QMessageBox.information(self, "Check for Updates", "No updates available.")

    def apply_theme(self, theme_name):
        styles_path = os.path.join(os.path.dirname(__file__), 'resources', 'styles', f"{theme_name}.qss")
        if os.path.exists(styles_path):
            with open(styles_path, 'r') as f:
                self.setStyleSheet(f.read())
            self.status_bar.show_message(f"{theme_name.capitalize()} theme applied.")
        else:
            self.status_bar.show_message("Theme file not found.")

    def toggle_theme(self):
        current_style = self.styleSheet()
        if "background-color: #2b2b2b;" in current_style or "background-color: #1e1e1e;" in current_style:
            self.apply_theme("light")
        else:
            self.apply_theme("dark")

    # Autosave
    def init_autosave(self):
        from PySide6.QtCore import QTimer 
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(300000) 

    def autosave(self):
        temp_dir = os.path.join(os.getenv('APPDATA'), 'NoteEditor2')
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, 'autosave.txt')
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            self.status_bar.show_message("Autosaved.")
        except Exception as e:
            self.status_bar.show_message(f"Autosave failed: {e}")
