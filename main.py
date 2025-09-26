import sys

from PyQt6.QtWidgets import QApplication

from src.main_windows import WeatherWindow


def main() -> int:
    """Entry point for exemples_chapitre_6."""
    app = QApplication(sys.argv)
    window = WeatherWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
