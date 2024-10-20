from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QTextCursor
from utils.helpers import count_words
import enchant

class SpellCheckHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.dictionary = enchant.Dict("en_US")
        except enchant.errors.DictNotFoundError:
            self.dictionary = None
        self.format = QTextCharFormat()
        self.format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.format.setUnderlineColor(QColor("red"))

    def highlightBlock(self, text):
        if not self.dictionary:
            return
        words = text.split()
        index = 0
        for word in words:
            if not self.dictionary.check(word) and word != "":
                start = text.find(word, index)
                if start != -1:
                    self.setFormat(start, len(word), self.format)
                    index = start + len(word)
            else:
                index += len(word) + 1  # +1 for the space 

class Editor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Segoe UI", 12))
        self.textChanged.connect(self.on_text_changed)
        self.word_count = 0
        self.highlighter = SpellCheckHighlighter(self.document())

    def on_text_changed(self):
        text = self.toPlainText()
        self.word_count = count_words(text)
        if self.parent() and hasattr(self.parent(), 'status_bar'):
            self.parent().status_bar.update_word_count(self.word_count)
