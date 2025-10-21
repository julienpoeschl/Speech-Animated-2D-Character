import numpy as np


class AudioInfo:
    """
    Container of immediately calulated data of audio bytes.
    """

    __slots__ = ("rms", "db", "dominant_freq", "audio_detected")

    def __init__(self, data : bytes, sample_rate : int = 44100, db_threshold : int = -40, compute_fft : bool = False) -> None:
        """
        Args:
            data (bytes): audio bytes to analyze.
            sample_rate (int): the rate at which to sample the frequencies.
            db_threshold (int): threshold at which audio is detected.
            compute_fft (bool): turns fast fourier transformation for optional frequence analysis.

        """
        
        samples = np.frombuffer(data, dtype=np.int16)
        samples = samples.astype(np.float32)
        
        rms = np.sqrt(np.mean(samples**2))
        if np.isnan(rms) or np.isinf(rms):
            rms = 0.0

        db = 20 * np.log10(rms / 32768)
        if np.isnan(db) or np.isinf(db):
            db = -100.0

        self.audio_detected = db > db_threshold

        self.rms = rms
        self.db = db

        if compute_fft:
            fft = np.fft.rfft(samples)
            freqs = np.fft.rfftfreq(len(samples), 1/sample_rate)
            magnitude = np.abs(fft)
            self.dominant_freq = freqs[np.argmax(magnitude)]
