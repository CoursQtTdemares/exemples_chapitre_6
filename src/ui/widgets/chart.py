from typing import override

from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QColor, QPainter, QPaintEvent, QPen
from PyQt6.QtWidgets import QWidget


class ExampleChart(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Définir une taille minimale pour que le widget soit visible
        self.setMinimumSize(400, 300)

    @override
    def paintEvent(self, event: QPaintEvent | None = None) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Obtenir les dimensions actuelles du widget
        width = self.width()
        height = self.height()

        # Définir les marges
        margin = 50
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin

        # Calculer les positions des points de manière relative
        # Point 1 : 10h, 20°C (1/3 de la largeur, température moyenne)
        point1 = QPointF(margin + chart_width * 0.2, margin + chart_height * 0.6)

        # Point 2 : 14h, 25°C (2/3 de la largeur, température haute)
        point2 = QPointF(margin + chart_width * 0.5, margin + chart_height * 0.3)

        # Point 3 : 18h, 18°C (fin, température basse)
        point3 = QPointF(margin + chart_width * 0.8, margin + chart_height * 0.8)

        # Background du graphique
        painter.fillRect(margin, margin, chart_width, chart_height, QColor(255, 255, 255))

        # Dessiner les points
        painter.setPen(QPen(QColor(255, 0, 0), 3))
        painter.drawEllipse(point1, 6, 6)
        painter.drawEllipse(point2, 6, 6)
        painter.drawEllipse(point3, 6, 6)

        # Dessiner les lignes
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.drawLine(point1, point2)
        painter.drawLine(point2, point3)

        # Etiquettes
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawText(point1 + QPointF(10, -10), "10h, 20°C")
        painter.drawText(point2 + QPointF(10, -10), "14h, 25°C")
        painter.drawText(point3 + QPointF(10, -10), "18h, 18°C")
