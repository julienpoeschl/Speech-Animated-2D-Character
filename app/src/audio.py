import pyaudio
from core.audio_analysis import AudioInfo


class AudioReader:
    def __init__(self) -> None:
        self._running = False
        self._curr_audio_info = None
        
        
    def start(self, p : pyaudio.PyAudio, device_index : int, format : int = pyaudio.paInt16, channel_count : int = 1, sample_rate : int = 44100, frames : int = 1024):
        
        self._running = True
        stream = p.open(format=format,
                        channels=channel_count,
                        rate=sample_rate,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=frames)

        while self._running:
            self.data = stream.read(1024)
            self._curr_audio_info = AudioInfo(self.data, sample_rate, -40)
            if self._curr_audio_info.audio_detected:
                print(self._curr_audio_info.db)



        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self._running = False


    @property
    def curr_audio_info(self) -> AudioInfo | None:
        return self._curr_audio_info
