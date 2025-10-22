import pyaudio
from core.pyaudio_devices import DeviceInfo
from .audio import AudioReader

from .frame_loader import MouthState

import threading

STARTING_FACE_TYPE = MouthState.Closed

class AppController:
    def __init__(self) -> None:
        self.py_audio = pyaudio.PyAudio()
        self.device_info = DeviceInfo(self.py_audio)
        self.audio_reader = AudioReader()
        self._curr_face_type = STARTING_FACE_TYPE


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
        self.audio_reader_thread = threading.Thread(target=self.audio_reader.start, args=(self.py_audio, self.curr_device_index))
        self.audio_reader_thread.start()

    def stop_reading_audio(self):
        if self.audio_reader_thread and self.audio_reader_thread.is_alive():
            self.audio_reader.stop()
            self.audio_reader_thread.join()

    def evaluate_audio(self) -> MouthState:
        audio_info = self.audio_reader.curr_audio_info
        if not audio_info:
            return STARTING_FACE_TYPE
        if not audio_info.audio_detected:
            return MouthState.Closed
        
        if audio_info.rms > 1000:
            return MouthState.Open
        elif audio_info.rms > 500:
            return MouthState.Intermediate
        
        return MouthState.Closed
    
    @property
    def running(self) -> bool:
        return self.audio_reader._running
    
    @property
    def curr_face_type(self) -> MouthState:
        return self._curr_face_type
    
    @property
    def db_volume_threshold(self) -> int:
        if not self.audio_reader._running:
            raise RuntimeError("ERROR: Trying to read volume from audio reader that isn't running.")
        if not self.audio_reader.curr_audio_info:
            return -60
        return int(self.audio_reader.curr_audio_info.db)
    
    @db_volume_threshold.setter
    def db_volume_threshold(self, value : int) -> None:
        self.audio_reader.db_threshold = value

    def set_db_volume_threshold(self, threshold : int) -> None:
        print(threshold)
        self.audio_reader.db_threshold = threshold
