from __future__ import annotations
from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class BBox:
    x1: float
    y1: float
    x2: float
    y2: float
    conf: float = 0.0
    cls: int = -1          # COCO-id

    # ────────── helper ─────────────────────────────────────────
    def as_xyxy(self) -> List[int]:
        return [int(self.x1), int(self.y1), int(self.x2), int(self.y2)]

    def iou(self, other: "BBox") -> float:
        ix1, iy1 = max(self.x1, other.x1), max(self.y1, other.y1)
        ix2, iy2 = min(self.x2, other.x2), min(self.y2, other.y2)
        inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
        if inter == 0:
            return 0.0
        a1 = (self.x2 - self.x1) * (self.y2 - self.y1)
        a2 = (other.x2 - other.x1) * (other.y2 - other.y1)
        return inter / (a1 + a2 - inter + 1e-6)

    # векторний IoU self × n×4 ndarray
    def iou_vec(self, others: np.ndarray) -> np.ndarray:
        x1 = np.maximum(self.x1, others[:, 0])
        y1 = np.maximum(self.y1, others[:, 1])
        x2 = np.minimum(self.x2, others[:, 2])
        y2 = np.minimum(self.y2, others[:, 3])
        inter = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
        a_self = (self.x2 - self.x1) * (self.y2 - self.y1)
        a_other = (others[:, 2] - others[:, 0]) * (others[:, 3] - others[:, 1])
        return inter / (a_self + a_other - inter + 1e-6)
