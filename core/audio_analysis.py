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
        
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768
        if len(samples) == 0:
            self.audio_detected = False
            return
        
        rms = np.sqrt(np.mean(samples**2))
        if np.isnan(rms) or np.isinf(rms):
            rms = 0.0

        db = 20 * np.log10(rms)
        if np.isnan(db) or np.isinf(db):
            db = -100.0

        zcr = np.mean(samples[:-1] * samples[1:] < 0)

        energy_threshold = 0.02
        # further testing
        is_speech = rms > energy_threshold and 0.02 < zcr < 0.25

        self.audio_detected = db > db_threshold

        self.rms : float = rms
        self.db : float = db

        if compute_fft:
            fft = np.fft.rfft(samples)
            freqs = np.fft.rfftfreq(len(samples), 1/sample_rate)
            magnitude = np.abs(fft)
            self.dominant_freq = freqs[np.argmax(magnitude)]
