from pathlib import Path
from typing import Any, override

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt

from src.api import WeatherResponse


class WeatherModel(QAbstractTableModel):
    def __init__(self, weather_data: list[WeatherResponse] | None = None) -> None:
        super().__init__()
        self.weather_data = weather_data or []

    @override
    def rowCount(self, parent: QModelIndex | None = None) -> int:
        return len(self.weather_data)

    @override
    def columnCount(self, parent: QModelIndex | None = None) -> int:
        return 3

    @override
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None

        if index.row() >= len(self.weather_data):
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            weather_item = self.weather_data[index.row()]
            if index.column() == 0:
                return weather_item["city"]
            elif index.column() == 1:
                return f"{weather_item['temperature']:.1f}°C"
            elif index.column() == 2:
                return f"{weather_item['humidity']}%"

        return None

    @override
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            headers = ["Ville", "Température", "Humidité"]
            if 0 <= section < len(headers):
                return headers[section]
        return None

    def add_weather_data(self, weather_data: WeatherResponse) -> None:
        self.beginInsertRows(QModelIndex(), len(self.weather_data), len(self.weather_data))

        self.weather_data.append(weather_data)

        self.endInsertRows()

    def export_to_csv(self, file_path: Path) -> None:
        title_columns = "Ville,Température,Humidité\n"
        file_path.write_text(title_columns + "\n".join(list(map(weather_data_to_csv_line, self.weather_data))))

    def load_from_csv(self, file_path: Path) -> None:
        self.beginResetModel()

        self.weather_data = [csv_line_to_weather_data(line) for line in file_path.read_text().split("\n")[1:]]

        self.endResetModel()


def weather_data_to_csv_line(weather_data: WeatherResponse) -> str:
    return ",".join(list(map(str, weather_data.values())))


def csv_line_to_weather_data(csv_line: str) -> WeatherResponse:
    city, temperature, humidity = csv_line.split(",")

    return {
        "city": city,
        "temperature": float(temperature),
        "humidity": float(humidity),
    }
