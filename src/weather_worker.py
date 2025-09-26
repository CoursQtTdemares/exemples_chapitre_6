from PyQt6.QtCore import QObject, QRunnable, pyqtSignal

from src import api


class WorkerSignals(QObject):
    received_weather_data = pyqtSignal(int, dict)  # worker_id, weather_data

    error_occurred = pyqtSignal(int, str)  # worker_id, error_message

    finished = pyqtSignal(int)  # worker_id


class WeatherWorker(QRunnable):
    def __init__(self, worker_id: int, city: str) -> None:
        super().__init__()
        self.worked_id = worker_id
        self.city = city
        self.signals = WorkerSignals()

    def run(self) -> None:
        try:
            weather_data = api.fetch_weather_data(self.city)
            self.signals.received_weather_data.emit(self.worked_id, weather_data)
        except Exception as e:
            self.signals.error_occurred.emit(self.worked_id, str(e))
        finally:
            self.signals.finished.emit(self.worked_id)
