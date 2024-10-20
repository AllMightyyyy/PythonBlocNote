from PySide6.QtWidgets import QToolBar, QStyle
from PySide6.QtGui import QIcon, QAction
import os

class ToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_toolbar()

    def init_toolbar(self):
        self.setMovable(False)

        # Define the path to icons
        icons_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'icons')

        # Function to safely create QIcons
        def create_icon(filename):
            icon_path = os.path.join(icons_path, filename)
            if os.path.exists(icon_path):
                return QIcon(icon_path)
            else:
                # Return a default icon if the specified one doesn't exist
                return self.parent.style().standardIcon(QStyle.SP_FileIcon)

        # New
        new_icon = create_icon('new.png')
        new_action = QAction(new_icon, "New", self)
        new_action.triggered.connect(self.parent.new_file)
        self.addAction(new_action)

        # Open
        open_icon = create_icon('open.png')
        open_action = QAction(open_icon, "Open", self)
        open_action.triggered.connect(self.parent.open_file)
        self.addAction(open_action)

        # Save
        save_icon = create_icon('save.png')
        save_action = QAction(save_icon, "Save", self)
        save_action.triggered.connect(self.parent.save_file)
        self.addAction(save_action)

        self.addSeparator()

        # Undo
        undo_icon = create_icon('undo.png')
        undo_action = QAction(undo_icon, "Undo", self)
        undo_action.triggered.connect(self.parent.editor.undo)
        self.addAction(undo_action)

        # Redo
        redo_icon = create_icon('redo.png')
        redo_action = QAction(redo_icon, "Redo", self)
        redo_action.triggered.connect(self.parent.editor.redo)
        self.addAction(redo_action)

        self.addSeparator()

        # Cut
        cut_icon = create_icon('cut.png')
        cut_action = QAction(cut_icon, "Cut", self)
        cut_action.triggered.connect(self.parent.editor.cut)
        self.addAction(cut_action)

        # Copy
        copy_icon = create_icon('copy.png')
        copy_action = QAction(copy_icon, "Copy", self)
        copy_action.triggered.connect(self.parent.editor.copy)
        self.addAction(copy_action)

        # Paste
        paste_icon = create_icon('paste.png')
        paste_action = QAction(paste_icon, "Paste", self)
        paste_action.triggered.connect(lambda checked: self.parent.editor.paste())
        self.addAction(paste_action)

        self.addSeparator()

        # Search (Find)
        search_icon = create_icon('search.png')
        search_action = QAction(search_icon, "Find", self)  # Properly define search_action
        search_action.triggered.connect(self.parent.find_replace_dialog.show)  # Show the find/replace dialog
        self.addAction(search_action)

        # Replace
        replace_icon = create_icon('replace.png')
        replace_action = QAction(replace_icon, "Replace", self)  # Properly define replace_action
        replace_action.triggered.connect(self.parent.find_replace_dialog.show)  # Show the find/replace dialog
        self.addAction(replace_action)

        self.addSeparator()

        # Theme Toggle Button
        theme_icon = self.parent.style().standardIcon(QStyle.SP_DesktopIcon)
        theme_action = QAction(theme_icon, "Toggle Theme", self)
        theme_action.triggered.connect(lambda checked: self.parent.toggle_theme())
        self.addAction(theme_action)
