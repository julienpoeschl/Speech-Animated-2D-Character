import sys

from PyQt6.QtWidgets import QApplication

from .gui.window import AppWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = AppWindow(app)
    window.open()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
