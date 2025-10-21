from PyQt6.QtWidgets import QApplication
import sys

from .controller import Controller
from .gui.window import AppWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    window = AppWindow(app, controller)
    window.show()
    sys.exit(app.exec())
