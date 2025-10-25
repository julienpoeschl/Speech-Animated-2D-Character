from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.src.constants import STARTING_FACE_TYPE

from ..frame_loader import FrameLoader, MouthState


class CharacterPanel(QWidget):
    """
    QWidget that displays a character frame.
    """

    def __init__(self, parent=None):
        """
        
        """
        super().__init__(parent)

        frame_loader = FrameLoader()

        layout = QVBoxLayout(self)

        # --- Character image ---
        character_label = QLabel()
        character_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(character_label)

        pixmap = frame_loader.get_frame_pixmap(STARTING_FACE_TYPE)
        character_label.setPixmap(pixmap)
        character_label.setScaledContents(True)

        self._character_label = character_label
        self._frame_loader = frame_loader


    def update(self, state : MouthState) -> None:
        """
        Get current character frame from frame loader and update the panel.
        """

        pixmap = self._frame_loader.get_frame_pixmap(state)
        self._character_label.setPixmap(pixmap)

    def stop(self) -> None:
        self.update(STARTING_FACE_TYPE)