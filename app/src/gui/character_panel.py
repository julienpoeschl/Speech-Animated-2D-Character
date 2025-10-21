from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from ..controller import Controller
from ..frame_loader import FrameLoader


class CharacterPanel(QWidget):
    def __init__(self, controller : Controller, parent=None):
        super().__init__(parent)

        self.controller = controller
        frame_loader = FrameLoader()
        self.frame_loader = frame_loader

        layout = QVBoxLayout(self)

        # Character image
        self.character_label = QLabel()
        self.character_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.character_label)

        pixmap = frame_loader.get_frame_pixmap(self.controller.curr_face_type)
        self.character_label.setPixmap(pixmap)
        self.character_label.setScaledContents(True)


    def update(self) -> None:
        curr_face_type = self.controller.evaluate_audio()
        pixmap = self.frame_loader.get_frame_pixmap(curr_face_type)
        self.character_label.setPixmap(pixmap)