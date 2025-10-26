import pyaudio

from core.pyaudio_devices import DeviceInfo

from .audio_evaluator import AudioEvaluator
from .audio_reader import AudioReader
from .frame_loader import MouthState


class AppController:
    def __init__(self) -> None:
        self.py_audio = pyaudio.PyAudio()
        self.device_info = DeviceInfo(self.py_audio)
        self.audio_reader = AudioReader(self.py_audio, self.device_info.default_device_index)
        self.audio_evaluator = AudioEvaluator()


    def get_device_names(self) -> list[str]:
        all_device_names = []
        for index in range(self.device_info.device_count):
            all_device_names.append(self.device_info.get_device_name(index))
        return all_device_names
    
    def get_default_device_index(self) -> int:
        return self.device_info.default_device_index

    def start_reading_audio(self) -> None:
        self.audio_reader.start()

    def stop_reading_audio(self) -> None:
        self.audio_reader.stop()

    def evaluate_audio(self) -> MouthState:
        audio_info = self.audio_reader.curr_audio_info
        return self.audio_evaluator.evaluate(audio_info)

    def get_volume(self) -> int:
        audio_info = self.audio_reader.curr_audio_info
        if audio_info is None:
            return -60
        return int(audio_info.db)

    def is_audio_reader_running(self) -> bool:
        return self.audio_reader.running

    def on_device_index_changed(self, index : int) -> None:
        print("New device selected: ", self.device_info.get_device_name(index))
        self.audio_reader.configure(device_index=index)

    def on_ambient_threshold_changed(self, value : int) -> None:
        print("New ambient threshold selected: ", value)
        self.audio_reader.configure(db_threshold=value)

    def on_speech_threshold_changed(self, value : int) -> None:
        print("New speech threshold selected: ", self.audio_reader.db_threshold + value)
        self.audio_evaluator.configure(speech_volume_threshold=self.audio_reader.db_threshold + value)
