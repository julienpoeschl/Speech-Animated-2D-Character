from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QComboBox, QHBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QScreen

from .controller import Controller
from .character_loader import load_character_as_pixmap

WINDOW_NAME = "Speech Animated Character - Demo"
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 400
DEFAULT_SCREEN_SIZE = QSize(1920, 1080)

CHARACTER_FPS = 30
CHARACTER_MS_FPS = int(1000 / CHARACTER_FPS)    



class AppWindow(QWidget):
    def __init__(self, screen : QScreen | None, controller : Controller):
        super().__init__()
        

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
        settings_layout = QVBoxLayout()
        main_layout.addLayout(settings_layout, 1)  # stretch factor 1

        # Example settings
        self.device_label = QLabel("Input Device:")
        settings_layout.addWidget(self.device_label)

        self.device_combo = QComboBox()
        self.device_combo.addItems(controller.get_device_names())  # populate dynamically later
        settings_layout.addWidget(self.device_combo)
        default_index = controller.get_default_device_index()
        self.device_combo.setCurrentIndex(default_index)
        self.device_combo.currentIndexChanged.connect(controller.on_device_index_changed)
        controller.on_device_index_changed(default_index)

        self.rms_threshold_label = QLabel("RMS Threshold:")
        settings_layout.addWidget(self.rms_threshold_label)

        self.rms_slider = QSlider(Qt.Orientation.Horizontal)
        self.rms_slider.setMinimum(0)
        self.rms_slider.setMaximum(10000)
        self.rms_slider.setValue(1000)
        settings_layout.addWidget(self.rms_slider)

        self.noise_gate_checkbox = QCheckBox("Enable Noise Gate")
        settings_layout.addWidget(self.noise_gate_checkbox)

        settings_layout.addStretch()  # push items to top

        # --- Right: Main content area ---
        main_area_layout = QVBoxLayout()
        main_layout.addLayout(main_area_layout, 3)  # stretch factor 3

        
        #self.status_label = QLabel("🎙️ Waiting for input...")
        #self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #main_area_layout.addWidget(self.status_label)

        self.character_label = QLabel()
        main_area_layout.addWidget(self.character_label)

        # Load PNG
        pixmap = load_character_as_pixmap(controller.curr_face_type)
        self.character_label.setPixmap(pixmap)

        print(self.character_label.geometry)

        # Optional: scale the image to fit the label
        self.character_label.setScaledContents(True)

        self.start_button = QPushButton("Start Listening")
        main_area_layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self._on_start_button)

        self.timer = QTimer()

        self.controller = controller

    def _on_start_button(self) -> None:
        if self.controller.running:
            self.timer.timeout.disconnect(self.update_frame)
            self.start_button.setText("Start Listening")
            self.controller.stop_reading_audio()
        else:
            self.start_button.setText("Listening...")
            self.controller.start_reading_audio()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(CHARACTER_MS_FPS)

    def update_frame(self) -> None:
        curr_face_type = self.controller.evaluate_audio()
        pixmap = load_character_as_pixmap(curr_face_type)
        self.character_label.setPixmap(pixmap)
        print(f"Updated face at framerate {CHARACTER_FPS}.")
