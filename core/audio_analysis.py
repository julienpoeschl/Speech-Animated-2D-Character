import numpy as np

class AudioInfo:
    
    def __init__(self, data : bytes, sample_rate : int = 44100, db_threshold : int = -40) -> None:
        samples = np.frombuffer(data, dtype=np.int16)
        samples = samples.astype(np.float32)
        rms = np.sqrt(np.mean(samples**2))
        if np.isnan(rms) or np.isinf(rms):
            rms = 0.0

        db = 20 * np.log10(rms / 32768)
        if np.isnan(db) or np.isinf(db):
            db = -100.0


        if db > db_threshold:
            print("Speech detected!", int(rms), "RMS, ", int(db), "db")
            self.audio_detected = True
        else:
            print("Silence.", int(rms), "RMS, ", int(db), "db")
            self.audio_detected = False

        fft = np.fft.rfft(samples)
        freqs = np.fft.rfftfreq(len(samples), 1/sample_rate)
        magnitude = np.abs(fft)

        self.rms = rms
        self.db = db
        self.dominant_freq = freqs[np.argmax(magnitude)]