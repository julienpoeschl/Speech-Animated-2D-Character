from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from ..controller import AppController
from ..frame_loader import FrameLoader, MouthState

STARTING_FACE_TYPE = MouthState.Closed

class CharacterPanel(QWidget):
    """
    QWidget that displays a character frame.
    """

    def __init__(self, controller : AppController, parent=None):
        """
        Args:
            controller (AppController): Application controller as interface to functionality.
        """
        super().__init__(parent)

        frame_loader = FrameLoader()

        layout = QVBoxLayout(self)

        # --- Character image ---
        self.character_label = QLabel()
        self.character_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.character_label)

        pixmap = frame_loader.get_frame_pixmap(STARTING_FACE_TYPE)
        self.character_label.setPixmap(pixmap)
        self.character_label.setScaledContents(True)

        self.controller = controller
        self.frame_loader = frame_loader


    def update(self) -> None:
        """
        Get current character frame from frame loader and update the panel.
        """
        curr_face_type = self.controller.evaluate_audio()
        pixmap = self.frame_loader.get_frame_pixmap(curr_face_type)
        self.character_label.setPixmap(pixmap)