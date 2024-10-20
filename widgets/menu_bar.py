from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QKeySequence, QAction
from PySide6.QtCore import Qt
from widgets.find_replace_dialog import FindReplaceDialog

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_menu()

    def init_menu(self):
        self.init_file_menu()
        self.init_edit_menu()
        self.init_view_menu()
        self.init_format_menu()
        self.init_tools_menu()
        self.init_help_menu()

    def init_file_menu(self):
        file_menu = self.addMenu("&File")

        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.parent.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.parent.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.parent.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.parent.save_file_as)
        file_menu.addAction(save_as_action)

        export_menu = file_menu.addMenu("Export")

        export_pdf = QAction("Export as PDF", self)
        export_pdf.triggered.connect(self.parent.export_as_pdf)
        export_menu.addAction(export_pdf)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)

    def init_edit_menu(self):
        edit_menu = self.addMenu("&Edit")

        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.parent.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.parent.editor.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.parent.editor.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.parent.editor.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(lambda checked: self.parent.editor.paste())
        edit_menu.addAction(paste_action)

        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.SelectAll)
        select_all_action.triggered.connect(self.parent.editor.selectAll)
        edit_menu.addAction(select_all_action)

        edit_menu.addSeparator()

        # Find in Edit Menu
        find_action = QAction("Find", self)
        find_action.setShortcut(QKeySequence.Find)
        find_action.triggered.connect(self.parent.find_replace_dialog.show) 
        edit_menu.addAction(find_action)

        # Replace in Edit Menu
        replace_action = QAction("Replace", self)
        replace_action.setShortcut(QKeySequence.Replace)
        replace_action.triggered.connect(self.parent.find_replace_dialog.show)  
        edit_menu.addAction(replace_action)

    def init_view_menu(self):
        view_menu = self.addMenu("&View")

        toggle_toolbar_action = QAction("Toggle Toolbar", self, checkable=True)
        toggle_toolbar_action.setChecked(True)
        toggle_toolbar_action.triggered.connect(self.parent.toggle_toolbar)
        view_menu.addAction(toggle_toolbar_action)

        toggle_statusbar_action = QAction("Toggle Status Bar", self, checkable=True)
        toggle_statusbar_action.setChecked(True)
        toggle_statusbar_action.triggered.connect(self.parent.toggle_statusbar)
        view_menu.addAction(toggle_statusbar_action)

        view_menu.addSeparator()

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence.ZoomIn)
        zoom_in_action.triggered.connect(self.parent.zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence.ZoomOut)
        zoom_out_action.triggered.connect(self.parent.zoom_out)
        view_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        reset_zoom_action.triggered.connect(self.parent.reset_zoom)
        view_menu.addAction(reset_zoom_action)

        # Add Toggle Theme Action
        toggle_theme_action = QAction("Toggle Theme", self, checkable=True)
        toggle_theme_action.setShortcut(QKeySequence("Ctrl+T"))
        toggle_theme_action.setChecked(False)  # Default to light theme
        toggle_theme_action.triggered.connect(self.parent.toggle_theme)
        view_menu.addAction(toggle_theme_action)

    def init_format_menu(self):
        format_menu = self.addMenu("F&ormat")

        font_action = QAction("Font", self)
        font_action.triggered.connect(self.parent.change_font)
        format_menu.addAction(font_action)

        text_color_action = QAction("Text Color", self)
        text_color_action.triggered.connect(self.parent.change_text_color)
        format_menu.addAction(text_color_action)

        bg_color_action = QAction("Background Color", self)
        bg_color_action.triggered.connect(self.parent.change_bg_color)
        format_menu.addAction(bg_color_action)

        format_menu.addSeparator()

        alignment_menu = format_menu.addMenu("Alignment")
        align_left = QAction("Left", self)
        align_left.triggered.connect(lambda: self.parent.editor.setAlignment(Qt.AlignLeft))
        alignment_menu.addAction(align_left)

        align_center = QAction("Center", self)
        align_center.triggered.connect(lambda: self.parent.editor.setAlignment(Qt.AlignCenter))
        alignment_menu.addAction(align_center)

        align_right = QAction("Right", self)
        align_right.triggered.connect(lambda: self.parent.editor.setAlignment(Qt.AlignRight))
        alignment_menu.addAction(align_right)

        align_justify = QAction("Justify", self)
        align_justify.triggered.connect(lambda: self.parent.editor.setAlignment(Qt.AlignJustify))
        alignment_menu.addAction(align_justify)

        bullets_action = QAction("Bullets", self)
        bullets_action.triggered.connect(self.parent.add_bullets)
        format_menu.addAction(bullets_action)

        numbering_action = QAction("Numbering", self)
        numbering_action.triggered.connect(self.parent.add_numbering)
        format_menu.addAction(numbering_action)

    def init_tools_menu(self):
        tools_menu = self.addMenu("&Tools")

        word_count_action = QAction("Word Count", self)
        word_count_action.triggered.connect(self.parent.show_word_count)
        tools_menu.addAction(word_count_action)

        spell_check_action = QAction("Spell Check", self)
        spell_check_action.triggered.connect(self.parent.spell_check)
        tools_menu.addAction(spell_check_action)

        thesaurus_action = QAction("Thesaurus", self)
        thesaurus_action.triggered.connect(self.parent.open_thesaurus)
        tools_menu.addAction(thesaurus_action)

        language_action = QAction("Language Selection", self)
        language_action.triggered.connect(self.parent.select_language)
        tools_menu.addAction(language_action)

    def init_help_menu(self):
        help_menu = self.addMenu("&Help")

        documentation_action = QAction("Documentation", self)
        documentation_action.triggered.connect(self.parent.open_documentation)
        help_menu.addAction(documentation_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.parent.show_about)
        help_menu.addAction(about_action)

        check_updates_action = QAction("Check for Updates", self)
        check_updates_action.triggered.connect(self.parent.check_updates)
        help_menu.addAction(check_updates_action)
