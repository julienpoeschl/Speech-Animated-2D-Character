import json
import os
import random
from enum import Enum

from PyQt6.QtGui import QPixmap

CONFIG_PATH = os.path.join("app", "assets", "configuration", "config.json")
ASSETS_DIR = os.path.join("app", "assets")
FRAMES_DIR = os.path.join(ASSETS_DIR, "frames")


class MouthState(Enum):
    Closed = 0
    Intermediate = 1
    Open = 2


class FrameLoader:
    """
    Loads and manages QPixmap frames for different mouth states based on a JSON config file.
    """

    def __init__(self) -> None:
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(f"Missing configuration file: {CONFIG_PATH}")

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in config file: {CONFIG_PATH}") from e

        layout_name = config.get("active_preset")
        if not layout_name:
            raise KeyError('Config file must contain an "active_preset" entry.')

        presets = config.get("presets")
        if layout_name not in presets:
            raise KeyError(f'Layout "{layout_name}" not found in config presets.')

        layout = presets[layout_name]
        try:
            closed_frame_path: str = layout["closed_mouth"]
            open_frame_path: str = layout["open_mouth"]
            intermediate_frame_paths: list[str] = layout["intermediate"]
        except KeyError as e:
            raise KeyError(f"Missing required key in layout '{layout_name}': {e.args[0]}")
        

        def load_frame(frame_name: str) -> QPixmap:
            """Load a frame image as a QPixmap from the frames directory."""
            path = os.path.join(FRAMES_DIR, frame_name)
            if not os.path.exists(path):
                raise FileNotFoundError(f"Frame file does not exist: {path}")
            
            pixmap = QPixmap(path)
            if pixmap.isNull():
                raise RuntimeError(f"Failed to load image: {path}")
            return pixmap

        self.closed_frame = load_frame(closed_frame_path)
        self.open_frame = load_frame(open_frame_path)
        self.intermediate_frames = [load_frame(p) for p in intermediate_frame_paths]

        print(
            f"Using layout '{layout_name}' with frames:\n"
            f"  Closed: {closed_frame_path}\n"
            f"  Open: {open_frame_path}\n"
            f"  Intermediate: {intermediate_frame_paths}"
        )

    def get_frame_pixmap(self, state: MouthState) -> QPixmap:
        """Return the QPixmap for the given face type."""

        if state == MouthState.Closed:
            return self.closed_frame
        elif state == MouthState.Open:
            return self.open_frame
        elif state == MouthState.Intermediate:
            return random.choice(self.intermediate_frames)
        else:
            raise ValueError(f"Unsupported face type: {state}")
