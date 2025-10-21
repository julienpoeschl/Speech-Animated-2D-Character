from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QHBoxLayout
from PyQt6.QtCore import Qt

from ..controller import Controller

class SettingsPanel(QWidget):
    def __init__(self, controller : Controller, parent=None):
        super().__init__(parent)

        self.controller = controller
        settings_layout = QVBoxLayout(self)

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

        self.db_threshold_label = QLabel("Audio level (dB):")
        settings_layout.addWidget(self.db_threshold_label)

        # --- Create slider ---
        self.db_volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.db_volume_slider.setMinimum(-60)   # typical dB min
        self.db_volume_slider.setMaximum(0)     # max volume (0 dB)
        self.db_volume_slider.setValue(-60)
        #self.db_threshold_slider.setDisabled(True)  # makes it uninteractable
        self.db_volume_slider.valueChanged.connect(controller.set_db_volume_threshold)
        settings_layout.addWidget(self.db_volume_slider)
        # --- Style the slider ---
        self.update_db_volume_slider(0.0)

        tick_layout = QHBoxLayout()
        settings_layout.addLayout(tick_layout)

        for db in range(-60, 1, 10):  # -60, -50, ..., 0
            lbl = QLabel(str(db))
            lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            tick_layout.addWidget(lbl)

        settings_layout.addStretch()  # push items to top



    def update_db_volume_slider(self, progress: float) -> None:
        """progress is a value between 0.0 (min) and 1.0 (max)"""
        # Convert progress to a CSS gradient stop
        # Blue → red gradient, tinted only up to progress
        if progress < 0 or progress > 1:
            raise RuntimeError("ERROR: Progress must be a value between 0.0 and 1.0.")
            
        gradient = f"""
            QSlider::groove:horizontal {{
                border: 1px solid #444;
                height: 20px;
                border-radius: 5px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0   #24853e,
                    stop: {progress + 0.001:.3f} #1e1e1e
                );
            }}
            QSlider::handle:horizontal {{
                background: #ffffff;
                width: 5px;
                margin: -2px 0;
                border-radius: 5px;
            }}
        """
        self.db_volume_slider.setStyleSheet(gradient)

    def update_volume(self):
        # simulate dB value between -60 and 0
        db = self.controller.db_volume
        #self.db_volume_slider.setValue(int(db))

        # convert dB range (-60..0) → (0..1)
        progress = (db + 60) / 60
        self.update_db_volume_slider(progress)