from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import QSize, QTimer

from ..controller import AppController
from .character_panel import CharacterPanel
from .settings_panel import SettingsPanel

WINDOW_NAME = "Speech Animated Character - Demo" # setting
WINDOW_WIDTH = 700 # setting
WINDOW_HEIGHT = 400 # setting
DEFAULT_SCREEN_SIZE = QSize(1920, 1080) # setting

WINDOW_FPS = 30 # setting
WINDOW_FPS_IN_MS = int(1000 / WINDOW_FPS)    



class AppWindow(QWidget):
    def __init__(self, app : QApplication, controller : AppController):
        super().__init__()

        self.controller = controller
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
        settings_panel = SettingsPanel(controller)
        main_layout.addWidget(settings_panel, 3)
        self.settings_panel = settings_panel


        # --- Right: Animated character panel ---
        character_panel = CharacterPanel(controller)
        main_layout.addWidget(character_panel, 3)
        self.character_panel = character_panel

        # --- Right: Start button ---
        self.start_button = QPushButton("Start Listening")
        self.start_button.clicked.connect(self._on_start_clicked)
        character_panel_layout = character_panel.layout()
        if character_panel_layout:
            character_panel_layout.addWidget(self.start_button)

        self.timer.start(WINDOW_FPS_IN_MS)


    def _on_start_clicked(self) -> None:
        if self.controller.running:
            self.timer.timeout.disconnect(self.character_panel.update)
            self.timer.timeout.disconnect(self.settings_panel.update_volume)
            self.start_button.setText("Start Listening")
            self.controller.stop_reading_audio()
        else:
            self.start_button.setText("Listening...")
            self.controller.start_reading_audio()
            self.timer.timeout.connect(self.character_panel.update)
            self.timer.timeout.connect(self.settings_panel.update_volume)

    def closeEvent(self, event):
        """
        This method is called automatically when the user tries to close the window.
        """

        if self.controller.running:
            self.timer.timeout.disconnect(self.character_panel.update)
            self.timer.timeout.disconnect(self.settings_panel.update_volume)
            self.start_button.setText("Start Listening")
            self.controller.stop_reading_audio()

        event.accept()
        # event.ignore()

