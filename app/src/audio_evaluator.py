from app.src.constants import DEFAULT_SPEECH_VOLUME_THRESHOLD
from core.audio_analysis import AudioInfo

from .frame_loader import MouthState


class AudioEvaluator:

    def __init__(self) -> None:
        self._speech_volume_threshold = DEFAULT_SPEECH_VOLUME_THRESHOLD


    def evaluate(self, audio_info : AudioInfo | None) -> MouthState:
        
        if audio_info is None or not audio_info.audio_detected:
            return MouthState.Closed
        if audio_info.db > self._speech_volume_threshold:
            return MouthState.Open
        else:
            return MouthState.Intermediate
    

    def configure(self, speech_volume_threshold : int | None = None) -> None:
        """
        Updates the settings of the audio reader with all provided new values.

        Args:
            db_threshold_speech (int): 
        """
        
        if speech_volume_threshold is None:
            raise RuntimeWarning("Configure was called on audio evaluator without any arguments. This does nothing and is redundant.")
        
        self._speech_volume_threshold = speech_volume_threshold
        