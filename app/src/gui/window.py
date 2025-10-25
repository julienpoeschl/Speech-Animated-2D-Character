from typing import Callable

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QWidget

from ..frame_loader import MouthState
from .character_panel import CharacterPanel
from .settings_panel import SettingsPanel

WINDOW_NAME = "Speech Animated Character - Demo" # setting
WINDOW_WIDTH = 700 # setting
WINDOW_HEIGHT = 400 # setting
DEFAULT_SCREEN_SIZE = QSize(1920, 1080) # setting

WINDOW_FPS = 60 # setting
WINDOW_FPS_IN_MS = int(1000 / WINDOW_FPS)    



class AppWindow(QWidget):
    def __init__(self, app : QApplication, device_names : list[str], default_device_index : int):
        super().__init__()


        self.timer = QTimer()
        screen = app.primaryScreen()

        if screen:
            screen_size = screen.size()
            print("Found screen size: (", DEFAULT_SCREEN_SIZE.width(), ", ", DEFAULT_SCREEN_SIZE.height(), ").")
        else:
            screen_size = DEFAULT_SCREEN_SIZE
            print("No screen size found. Default size of (", DEFAULT_SCREEN_SIZE.width(), ", ", DEFAULT_SCREEN_SIZE.height(), ") used.")

        self.setWindowTitle("🎙️ " + WINDOW_NAME)
        self.setGeometry(screen_size.width() // 2 - WINDOW_WIDTH // 2, screen_size.height() // 2 - WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT)

        # --- Main horizontal layout ---
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        

        # --- Left: Settings panel ---
        settings_panel = SettingsPanel(device_names, default_device_index)
        main_layout.addWidget(settings_panel, 3)
        self._settings_panel = settings_panel


        # --- Right: Animated character panel ---
        character_panel = CharacterPanel()
        main_layout.addWidget(character_panel, 3)
        self.character_panel = character_panel

        # --- Right: Start button ---
        self._start_button = QPushButton("Start Listening")
        character_panel_layout = character_panel.layout()
        if character_panel_layout:
            character_panel_layout.addWidget(self._start_button)


    def listen_start_button_clicked(self, func : Callable[[], None]) -> None:
        """Subscribe to start button clicked event."""
        self._start_button.clicked.connect(func)

    def stop_listen_event(self) -> None:
        self.timer.stop()
        self.character_panel.stop()
        self._settings_panel.stop()
        self._start_button.setText("Start Listening")

    def start_listen_event(self, state_callback : Callable[[], MouthState], volume_callback : Callable[[], int]) -> None:
        self.timer.start(WINDOW_FPS_IN_MS)
        self._start_button.setText("Stop Listening")

        def listen(state_callback : Callable[[], MouthState], volume_callback : Callable[[], int]) -> None:
            self.character_panel.update(state_callback())
            self._settings_panel.update(volume_callback())

        self.timer.timeout.connect(lambda: listen(state_callback, volume_callback))


    def listen_device_combo_index_changed(self, func : Callable[[int], None]) -> None:
        self._settings_panel.listen_device_combo_index_changed(func)

    def listen_ambient_cutoff_threshold_slider_value_changed(self, ambient_cuttoff_callback : Callable[[int], None], speech_threshold_callback : Callable[[int], None]) -> None:
        self._settings_panel.listen_ambient_cutoff_threshold_slider_value_changed(ambient_cuttoff_callback, speech_threshold_callback)

    def listen_speech_threshold_spinBox_value_changed(self, func : Callable[[int], None]) -> None:
        self._settings_panel.listen_speech_threshold_spinBox_value_changed(func)

    def closeEvent(self, event):
        """
        This method is called automatically when the user tries to close the window.
        """

        self.timer.stop()

        event.accept()
        # event.ignore()

