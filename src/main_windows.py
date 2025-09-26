from pathlib import Path

from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QPushButton, QTableView, QVBoxLayout, QWidget

from src.api import WeatherResponse
from src.model import WeatherModel
from src.weather_worker import WeatherWorker

CITIES = ["Paris", "London", "Berlin", "Madrid", "Rome"]


class WeatherWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Weather Window")
        self.setGeometry(100, 100, 800, 600)

        self.model = WeatherModel()
        self.thread_pool = QThreadPool()

        self.setup_actions()
        self.setup_menubar()

        self.setup_ui()

    def setup_actions(self) -> None:
        self.save_action = QAction("Export to CSV", self)
        self.save_action.triggered.connect(self.export_to_csv)

        self.load_action = QAction("Load from CSV", self)
        self.load_action.triggered.connect(self.load_from_csv)

        self.quit_action = QAction("Quit", self)
        self.quit_action.triggered.connect(self.close)

    def export_to_csv(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.model.export_to_csv(Path(file_path))

    def load_from_csv(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Load from CSV", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.model.load_from_csv(Path(file_path))

    def setup_menubar(self) -> None:
        if (menubar := self.menuBar()) is None:
            return

        if (file_menu := menubar.addMenu("File")) is None:
            return

        file_menu.addAction(self.save_action)
        file_menu.addAction(self.load_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

    def setup_ui(self) -> None:
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        vertical_layout = QVBoxLayout()
        self.central_widget.setLayout(vertical_layout)

        self.download_button = QPushButton("Fetch Weather Data")
        self.download_button.clicked.connect(self.fetch_weather_data)

        self.view = QTableView()
        self.view.setModel(self.model)

        vertical_layout.addWidget(self.download_button)
        vertical_layout.addWidget(self.view)

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
        self.model.add_weather_data(weather_data)

    def display_error(self, worker_id: int, error_message: str) -> None:
        print(f"Worker {worker_id} failed: {error_message}")

    def worker_finished(self, worker_id: int) -> None:
        print(f"Worker {worker_id} finished.")
