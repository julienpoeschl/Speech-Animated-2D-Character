
from ..controller import AppController
from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QWidget

from .character_panel import CharacterPanel
from .settings_panel import SettingsPanel

WINDOW_NAME = "Speech Animated Character - Demo" # setting
WINDOW_WIDTH = 700 # setting
WINDOW_HEIGHT = 400 # setting
DEFAULT_SCREEN_SIZE = QSize(1920, 1080) # setting

WINDOW_FPS = 60 # setting
WINDOW_FPS_IN_MS = int(1000 / WINDOW_FPS)    



class AppWindow(QWidget):
    def __init__(self, app : QApplication):
        super().__init__()


        self.timer = QTimer()
        screen = app.primaryScreen()
        controller = AppController()
        self._controller = controller

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
        settings_panel = SettingsPanel(controller.get_device_names(), controller.get_default_device_index(), controller.on_device_index_changed, controller.on_ambient_threshold_changed, controller.on_speech_threshold_changed)
        main_layout.addWidget(settings_panel, 3)
        self._settings_panel = settings_panel


        # --- Right: Animated character panel ---
        character_panel = CharacterPanel()
        main_layout.addWidget(character_panel, 3)
        self._character_panel = character_panel

        # --- Right: Start button ---
        self._start_button = QPushButton("Start Listening")
        character_panel_layout = character_panel.layout()
        if character_panel_layout:
            character_panel_layout.addWidget(self._start_button)
            self._start_button.clicked.connect(self.on_start_button_clicked)

        self.timer.timeout.connect(lambda: self._character_panel.update(self._controller.evaluate_audio()))
        self.timer.timeout.connect(lambda: self._settings_panel.update(self._controller.get_volume()))


    def on_start_button_clicked(self) -> None:
        if self._controller.is_audio_reader_running():
            self.timer.stop()
            self._character_panel.stop()
            self._settings_panel.stop()
            self._start_button.setText("Start Listening")
            self._controller.stop_reading_audio()
        else:
            self._controller.start_reading_audio()
            self.timer.start(WINDOW_FPS_IN_MS)
            self._start_button.setText("Listening... (Press again to stop)")


    def open(self) -> None:
        """Starts the window."""
        self.show()


    def closeEvent(self, event):
        """
        This method is called automatically when the user tries to close the window.
        """

        self.timer.stop()

        event.accept()
        # event.ignore()

