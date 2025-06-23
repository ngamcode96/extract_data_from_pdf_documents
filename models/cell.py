from .bbox import Bbox

class Cell:
    def __init__(self, text: str, bbox: Bbox):
        self.text = text
        self.bbox = bbox
    
