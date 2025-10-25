import pyaudio
from PyQt6.QtWidgets import QApplication

from core.pyaudio_devices import DeviceInfo

from .audio_evaluator import AudioEvaluator
from .audio_reader import AudioReader
from .frame_loader import MouthState
from .gui.window import AppWindow


class AppController:
    def __init__(self, app : QApplication) -> None:
        self.py_audio = pyaudio.PyAudio()
        self.device_info = DeviceInfo(self.py_audio)
        self.audio_reader = AudioReader(self.py_audio)
        self.audio_evaluator = AudioEvaluator()

        curr_device_index = self.get_default_device_index()
        self._curr_device_index = curr_device_index
        window = AppWindow(app, self.get_device_names(), curr_device_index)
        window.listen_start_button_clicked(self.on_start_button_clicked)
        window.listen_device_combo_index_changed(self.on_device_index_changed)

        window.listen_ambient_cutoff_threshold_slider_value_changed(self.on_ambient_threshold_changed, self.on_speech_threshold_changed)
        window.listen_speech_threshold_spinBox_value_changed(self.on_speech_threshold_changed)

        self._window = window



    def on_start_button_clicked(self) -> None:
        if self.running:
            self._window.stop_listen_event()
            self.stop_reading_audio()
        else:
            self.start_reading_audio()
            self._window.start_listen_event(self.evaluate_audio, self.get_volume)


    def start_application(self) -> None:
        """Starts the window."""
        self._window.show()


    def get_device_names(self) -> list[str]:
        all_device_names = []
        for index in range(self.device_info.device_count):
            all_device_names.append(self.device_info.get_device_name(index))
        return all_device_names
    
    def get_default_device_index(self) -> int:
        return self.device_info.default_device_index

    def on_device_index_changed(self, index : int):
        print("New device selected: ", self.device_info.get_device_name(index))
        self._curr_device_index = index


    def start_reading_audio(self) -> None:
        self.audio_reader.start(self._curr_device_index)

    def stop_reading_audio(self):
        self.audio_reader.stop()

    def evaluate_audio(self) -> MouthState:
        audio_info = self.audio_reader.curr_audio_info
        return self.audio_evaluator.evaluate(audio_info)
    
    @property
    def running(self) -> bool:
        return self.audio_reader._running

    def get_volume(self) -> int:
        audio_info = self.audio_reader.curr_audio_info
        if audio_info is None:
            return -60
        return int(audio_info.db)

    def on_ambient_threshold_changed(self, value : int) -> None:
        print("New ambient threshold selected: ", value)
        self.audio_reader.configure(db_threshold=value)

    def on_speech_threshold_changed(self, value : int) -> None:
        print("New speech threshold selected: ", self.audio_reader.db_threshold + value)
        self.audio_evaluator.configure(speech_volume_threshold=self.audio_reader.db_threshold + value)
