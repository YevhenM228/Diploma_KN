import cv2
from typing import Dict
from utils.bbox import BBox


def corner_box(img, box: BBox, color=(0, 255, 0), lw=2, frac=0.18):
    x1, y1, x2, y2 = map(int, box.as_xyxy())
    w, h = x2 - x1, y2 - y1
    dx, dy = int(w * frac), int(h * frac)
    for sx, sy in [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]:
        ex = sx + dx if sx == x1 else sx - dx
        ey = sy + dy if sy == y1 else sy - dy
        cv2.line(img, (sx, sy), (ex, sy), color, lw)
        cv2.line(img, (sx, sy), (sx, ey), color, lw)


def overlay_stats(img, fps: float, counts: Dict[str, int]):
    cv2.putText(img, f"FPS:{fps:5.1f}  Vehicles:{sum(counts.values())}",
                (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    y = 50
    for cls in ("car"):
        if counts.get(cls):
            cv2.putText(img, f"{cls}:{counts[cls]}",
                        (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 2)
            y += 22
def put_label(img, text, x, y, color=(0, 255, 0), scale=0.6):
    """
    Короткий хелпер над cv2.putText:
    """
    cv2.putText(
        img, str(text),
        (int(x), int(y)),
        cv2.FONT_HERSHEY_SIMPLEX,
        scale, color, 2
    )