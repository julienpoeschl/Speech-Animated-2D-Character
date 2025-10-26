from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QSlider, QSpinBox, QVBoxLayout, QWidget

from app.src.constants import DEFAULT_DB_THRESHOLD, MAX_DB, MIN_DB, MIN_SPEECH_DB


class SettingsPanel(QWidget):
    """
    QWidget that contains interactable settings.
    """

    @property
    def device_index(self) -> int:
        return self._device_combo.currentIndex()

    def __init__(self, device_names : list[str], default_device_index : int, device_changed_callback : Callable[[int], None], ambient_threshold_changed_callback : Callable[[int], None], speech_threshold_changed_callback : Callable[[int], None], parent = None):
        """
            Args:
                device_names (list[str]): All available audio device names.
                default_device_index (int): Index of default device.
        """
        super().__init__(parent)

        layout = QVBoxLayout(self)

        device_label = QLabel("Input Device:")
        layout.addWidget(device_label)

 
        device_combo = QComboBox()
        device_combo.addItems(device_names)
        layout.addWidget(device_combo)
        default_index = default_device_index
        device_combo.setCurrentIndex(default_index)
        self._device_combo = device_combo
        device_combo.currentIndexChanged.connect(device_changed_callback)



        ambient_cutoff_threshold_label = QLabel("Ambient/Ignore Threshold (dB):")
        layout.addWidget(ambient_cutoff_threshold_label)

        ambient_cutoff_threshold_slider = QSlider(Qt.Orientation.Horizontal)
        ambient_cutoff_threshold_slider.setMinimum(MIN_DB)
        ambient_cutoff_threshold_slider.setMaximum(MAX_DB)
        ambient_cutoff_threshold_slider.setValue(DEFAULT_DB_THRESHOLD)
        #self.db_threshold_slider.setDisabled(True)  # makes it uninteractable
        layout.addWidget(ambient_cutoff_threshold_slider)

        self._ambient_cutoff_threshold_slider = ambient_cutoff_threshold_slider
        ambient_cutoff_threshold_slider.valueChanged.connect(ambient_threshold_changed_callback)
    
        self.update(MIN_DB)

        tick_layout = QHBoxLayout()
        layout.addLayout(tick_layout)

        for db in range(MIN_DB, MAX_DB + 1, 10):
            lbl = QLabel(str(db))
            lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            tick_layout.addWidget(lbl)


        speech_threshold_label = QLabel("Speech Threshold (dB):")
        layout.addWidget(speech_threshold_label)

        speech_threshold_spinBox = QSpinBox()
        speech_threshold_spinBox.setMinimum(MIN_SPEECH_DB)
        
        def update_speech_spinBox_max() -> None:
            # maybe clamp value before
            max_speech_threshold = abs(ambient_cutoff_threshold_slider.value())
            speech_threshold_spinBox.setMaximum(max_speech_threshold)

        update_speech_spinBox_max()
        ambient_cutoff_threshold_slider.valueChanged.connect(update_speech_spinBox_max)
        ambient_cutoff_threshold_slider.valueChanged.connect(lambda: speech_threshold_changed_callback(speech_threshold_spinBox.value()))

        speech_threshold_spinBox.valueChanged.connect(speech_threshold_changed_callback)
        speech_threshold_spinBox.setValue(MIN_SPEECH_DB)

        layout.addWidget(speech_threshold_spinBox)
        self._speech_threshold_spinBox = speech_threshold_spinBox

        layout.addStretch()



    def update(self, volume : int) -> None:
        """
        Args:
            volume (int): Decibel volume.
        """
        # convert dB range (-60..0) → (0..1)
        progress = (volume + 60) / 60

        def update_ambient_cutoff_threshold_slider(progress: float) -> None:
            """progress is a value between 0.0 (min) and 1.0 (max)"""

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
            self._ambient_cutoff_threshold_slider.setStyleSheet(gradient)
    
        update_ambient_cutoff_threshold_slider(progress)


    def stop(self) -> None:
        self.update(-60)