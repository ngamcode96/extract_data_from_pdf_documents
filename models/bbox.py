from dataclasses import dataclass, field

@dataclass
class Bbox:
    left: float = 0.0
    right: float = 0.0
    top: float = 0.0
    bottom: float = 0.0

    @classmethod
    def from_pdfplumber(cls, bbox: dict):
        return cls(
            left=bbox["x0"],
            top=bbox["top"],
            right=bbox["x1"],
            bottom=bbox["bottom"]
        )


    def to_pdfplumber(self):
        return {"x0": self.left, "top": self.top, "x1": self.right, "bottom": self.bottom}

    def union(self, bbox, tol=0):

        if self.top > bbox.top:
            self, bbox = bbox, self

        self.left = min(self.left, bbox.left)
        self.right = max(self.right, bbox.right)
        self.top = min(self.top, bbox.top)
        self.bottom = max(self.bottom, bbox.bottom)

        return self