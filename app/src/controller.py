import pyaudio
from core.pyaudio_devices import DeviceInfo
from .audio_reader import AudioReader
from .audio_evaluator import AudioEvaluator

from .frame_loader import MouthState

class AppController:
    def __init__(self) -> None:
        self.py_audio = pyaudio.PyAudio()
        self.device_info = DeviceInfo(self.py_audio)
        self.audio_reader = AudioReader(self.py_audio)
        self.audio_evaluator = AudioEvaluator()


    def get_device_names(self) -> list[str]:
        all_device_names = []
        for index in range(self.device_info.device_count):
            all_device_names.append(self.device_info.get_device_name(index))
        return all_device_names
    
    def get_default_device_index(self) -> int:
        return self.device_info.default_device_index

    def on_device_index_changed(self, index : int):
        print(index)
        self.curr_device_index = index


    def start_reading_audio(self) -> None:
        self.audio_reader.start(self.curr_device_index)

    def stop_reading_audio(self):
        self.audio_reader.stop()

    def evaluate_audio(self) -> MouthState:
        audio_info = self.audio_reader.curr_audio_info
        return self.audio_evaluator.evaluate(audio_info)
    
    @property
    def running(self) -> bool:
        return self.audio_reader._running

    
    @property
    def db_volume_threshold(self) -> int:
        if not self.audio_reader._running:
            raise RuntimeError("ERROR: Trying to read volume from audio reader that isn't running.")
        if not self.audio_reader.curr_audio_info:
            return -60
        return int(self.audio_reader.curr_audio_info.db)
    
    @db_volume_threshold.setter
    def db_volume_threshold(self, value : int) -> None:
        self.audio_reader.configure(db_threshold=value)

    def set_db_volume_threshold(self, value : int) -> None:

        self.audio_reader.configure(db_threshold=value)

    def on_speech_volume_threshold_valueChanged(self, value : int) -> None:

        self.audio_evaluator.configure(speech_volume_threshold=self.audio_reader.db_threshold + value)
