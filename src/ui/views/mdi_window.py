from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QMdiArea,
    QMdiSubWindow,
    QWidget,
)

from src.ui.widgets.form_widget import FormWidget
from src.ui.widgets.text_edit import TextEdit


class MDIWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MDI Window")
        self.setGeometry(100, 100, 800, 600)

        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        self.create_initial_documents()

    def create_initial_documents(self) -> None:
        self.create_document(TextEdit(), "Document Texte")
        self.create_document(FormWidget(), "Input Button Document")

    def create_document(self, widget: QWidget, title: str = "Input Button Document") -> None:
        # Create une sous fenetre
        sub_window = QMdiSubWindow()
        sub_window.setWidget(widget)
        sub_window.setWindowTitle(title)
        sub_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # On ajoute la sous fenetre a la zone MDI
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
