from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget


class FormWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Form Widget")
        self.setGeometry(100, 100, 800, 600)

        vertical_layout = QVBoxLayout()

        horizontal_layout = QHBoxLayout()
        label = QLabel("Entrez votre nom:")
        button = QPushButton("Valider")
        button.clicked.connect(self.handle_button_click)

        horizontal_layout.addWidget(label)
        horizontal_layout.addWidget(button)

        self.text_edit = QTextEdit("Hello, World!")
        self.text_edit.setReadOnly(True)

        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.text_edit)

        self.setLayout(vertical_layout)

    def handle_button_click(self) -> None:
        self.text_edit.append("clicked")
