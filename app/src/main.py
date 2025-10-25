import sys

from PyQt6.QtWidgets import QApplication

from .controller import AppController


def main() -> None:
    app = QApplication(sys.argv)
    controller = AppController(app)
    controller.start_application()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
