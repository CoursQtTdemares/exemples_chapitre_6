from PyQt6.QtWidgets import QTextEdit


class TextEdit(QTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.setPlainText("Hello, World!")
