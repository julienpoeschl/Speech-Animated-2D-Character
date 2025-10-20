from PyQt6.QtGui import QPixmap
from enum import Enum

class FaceType(Enum):
    Closed = 0,
    HalfOpen = 1
    LeftOpen = 2
    RightOpen = 3
    Open = 4

def load_character_as_pixmap(face_type : FaceType) -> QPixmap:
    
    match face_type:
        case FaceType.Closed:
            pixmap = QPixmap("app/media/character_1.png")
        case FaceType.HalfOpen:
            pixmap = QPixmap("app/media/character_5.png")
        case FaceType.LeftOpen:
            pixmap = QPixmap("app/media/character_2.png")
        case FaceType.RightOpen:
            pixmap = QPixmap("app/media/character_3.png")
        case FaceType.Open:
            pixmap = QPixmap("app/media/character_4.png")
        case _:
            raise RuntimeError("ERROR: Selected face type isn't supported or doesn't exist.")

    if not pixmap or pixmap.isNull():
        print("PNG couldn't be loaded.")
    return pixmap