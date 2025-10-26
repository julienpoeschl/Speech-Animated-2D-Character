import threading

from pyaudio import PyAudio

from app.src.constants import (
    DEFAULT_CHANNEL_COUNT,
    DEFAULT_DB_THRESHOLD,
    DEFAULT_FORMAT,
    DEFAULT_FRAMES,
    DEFAULT_SAMPLE_RATE,
)
from core.audio_analysis import AudioInfo


class AudioReader:
    """
    Audio reader is used to read from a PyAudio and creating Audio info instances.

    Properties:
    - db_threshold
    - fromat
    - channel_count
    - sample_rate
    - frames

    Methods:
    - configure()
    - start()
    - stop()
    - close()
    """


    @property
    def curr_audio_info(self) -> AudioInfo | None:
        """
        The audio info of the currently read audio bytes.
        """
        return self._curr_audio_info

    @property
    def db_threshold(self) -> int:
        return self._db_threshold
    
    @property
    def running(self) -> bool:
        return self._running

    
    def __init__(self, p : PyAudio, default_device_index : int):
        """
        Args:
            p (PyAudio): 
        """
        self._running = False
        self._thread = None
        self._curr_audio_info = None
        self._p = p
        self._stream = None

        self._device_index = default_device_index
        self._db_threshold = DEFAULT_DB_THRESHOLD
        self._format = DEFAULT_FORMAT
        self._channel_count = DEFAULT_CHANNEL_COUNT
        self._sample_rate = DEFAULT_SAMPLE_RATE
        self._frames = DEFAULT_FRAMES


    def start(self):
        """
        Starts a new thread to continuously read audio from an input audio device. Can get stopped by calling stop().
        """
        if self._running:
            raise RuntimeWarning("Audio reader already running.")
        
        def inner_read_loop():

            if not self._p:
                raise RuntimeError("ERROR")
            self._stream = self._p.open(format=self._format,
                                        channels=self._channel_count,
                                        rate=self._sample_rate,
                                        input=True,
                                        input_device_index=self._device_index,
                                        frames_per_buffer=self._frames)
            try:
                while self._running:
                    data = self._stream.read(self._frames, exception_on_overflow=False)
                    self._curr_audio_info = AudioInfo(data, self._sample_rate, self._db_threshold)
                    if self._curr_audio_info.audio_detected:
                        #print(self._curr_audio_info.db)
                        pass
            finally:
                self._stream.stop_stream()
                self._stream.close()
                self._stream = None

        self._running = True
        self._thread = threading.Thread(target=inner_read_loop, args=(), daemon=True)
        self._thread.start()

    def stop(self):
        """
        Stops the audio reader thread immediatly.
        """

        if not self._running:
            raise RuntimeWarning("Audio reader was tried to stop but didn't ran.")
        self._running = False
        if not self._thread:
            raise RuntimeWarning("Audio reader thread doesn't exist but was tried to stop.")
        self._thread.join()
        self._thread = None

        if self._curr_audio_info is None:
            raise RuntimeWarning("Current audio info couldn't be removed since it didn't exist.")
        self._curr_audio_info = None

    def close(self) -> None:
        """
        Cleanly close the audio reader.
        """

        if self._p:
            self._p.terminate()
            self._p = None

    def configure(self, device_index : int | None = None, db_threshold : int | None = None, format : int | None= None, channel_count : int | None= None, sample_rate : int | None = None, frames : int | None = None) -> None:
        """
        Updates the settings of the audio reader with all provided new values.

        Args:
            device_index (int): 
            db_threshold (int): 
            format (int):
            channel_count (int):
            sample_rate (int):
            frames (int):
        """
        
        if all(arg is None for arg in (device_index, db_threshold, format, channel_count, sample_rate, frames)):
            raise RuntimeWarning("Configure was called on audio reader without any arguments. This does nothing and is redundant.")
        
        if device_index is not None:
            self._device_index = device_index
        if db_threshold is not None:
            self._db_threshold = db_threshold
        if format is not None:
            self._format = format
        if channel_count is not None:    
            self._channel_count = channel_count
        if sample_rate is not None:
            self._sample_rate = sample_rate
        if frames is not None:
            self._frames = frames