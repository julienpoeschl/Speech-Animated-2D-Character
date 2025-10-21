from PyQt6.QtWidgets import QApplication
import sys

from .controller import AppController
from .gui.window import AppWindow


def main() -> None:
    app = QApplication(sys.argv)
    controller = AppController()
    window = AppWindow(app, controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
