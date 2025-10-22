from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QHBoxLayout
from PyQt6.QtCore import Qt

from ..controller import AppController

class SettingsPanel(QWidget):
    """
    QWidget that contains interactable settings.
    """

    def __init__(self, controller : AppController, parent=None):
        """
        Args:
            controller (AppController): Application controller as interface to functionality.
        """
        super().__init__(parent)

        self.controller = controller
        layout = QVBoxLayout(self)

        self.device_label = QLabel("Input Device:")
        layout.addWidget(self.device_label)

 
        self.device_combo = QComboBox()
        self.device_combo.addItems(controller.get_device_names())
        layout.addWidget(self.device_combo)
        default_index = controller.get_default_device_index()
        self.device_combo.setCurrentIndex(default_index)
        self.device_combo.currentIndexChanged.connect(controller.on_device_index_changed)
        controller.on_device_index_changed(default_index)


        self.db_threshold_label = QLabel("Audio level (dB):")
        layout.addWidget(self.db_threshold_label)

        self.db_volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.db_volume_slider.setMinimum(-60)   # typical dB min
        self.db_volume_slider.setMaximum(0)     # max volume (0 dB)
        self.db_volume_slider.setValue(-60)
        #self.db_threshold_slider.setDisabled(True)  # makes it uninteractable
        self.db_volume_slider.valueChanged.connect(controller.set_db_volume_threshold)
        layout.addWidget(self.db_volume_slider)

        self.update_db_volume_slider(0.0)

        tick_layout = QHBoxLayout()
        layout.addLayout(tick_layout)

        for db in range(-60, 1, 10):
            lbl = QLabel(str(db))
            lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            tick_layout.addWidget(lbl)


        layout.addStretch()  # push items to top



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
        db = self.controller.db_volume_threshold
        #self.db_volume_slider.setValue(int(db))

        # convert dB range (-60..0) → (0..1)
        progress = (db + 60) / 60
        self.update_db_volume_slider(progress)