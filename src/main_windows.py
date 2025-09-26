from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget

from src.api import WeatherResponse
from src.weather_worker import WeatherWorker

CITIES = ["Paris", "London", "Berlin", "Madrid", "Rome"]


class WeatherWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Weather Window")
        self.setGeometry(100, 100, 800, 600)

        self.thread_pool = QThreadPool()

        self.setup_ui()

    def setup_ui(self) -> None:
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        vertical_layout = QVBoxLayout()
        self.central_widget.setLayout(vertical_layout)

        self.download_button = QPushButton("Fetch Weather Data")
        self.download_button.clicked.connect(self.fetch_weather_data)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        vertical_layout.addWidget(self.download_button)
        vertical_layout.addWidget(self.text_edit)

    def fetch_weather_data(self) -> None:
        for worker_id, city in enumerate(CITIES, start=1):
            worker = WeatherWorker(worker_id, city)

            # connect the signals
            worker.signals.received_weather_data.connect(self.display_weather_data)
            worker.signals.error_occurred.connect(self.display_error)
            worker.signals.finished.connect(self.worker_finished)

            # start the worker
            self.thread_pool.start(worker)

    def display_weather_data(self, worker_id: int, weather_data: WeatherResponse) -> None:
        print(f"Worker {worker_id} succeeded.")
        self.text_edit.append(f"{weather_data['city']}: {weather_data['temperature']}°C, {weather_data['humidity']}%")

    def display_error(self, worker_id: int, error_message: str) -> None:
        self.text_edit.append(f"Worker {worker_id} failed: {error_message}")

    def worker_finished(self, worker_id: int) -> None:
        print(f"Worker {worker_id} finished.")
