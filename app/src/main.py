from PyQt6.QtWidgets import QApplication
import sys

from .controller import Controller
from .window import AppWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    screen = app.primaryScreen()
    window = AppWindow(screen, controller)
    window.show()
    sys.exit(app.exec())
