from __future__ import annotations
import csv
import json
from typing import Any, Dict, List, Mapping
import numpy as np

COCO_ID2NAME: Dict[int, str] = {
    2: "car"
}

def _bbox_to_str(bbox: List[int] | np.ndarray) -> str:
    """Перетворює [x1, y1, x2, y2] → 'x1 y1 x2 y2'."""
    bbox = np.asarray(bbox, dtype=int).tolist()
    return " ".join(map(str, bbox)) if len(bbox) == 4 else ""


def write_csv(objects_data: Mapping[int, Dict[str, Any]], csv_path: str) -> None:
    """Зберігає детальну інформацію про об’єкти у CSV."""
    headers = [
        "id",
        "vehicle_type",
        "vehicle_bbox",
        "lp_bbox",
        "lp_bbox_score",
        "frame_start",
        "frame_end",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)

        for tid, info in objects_data.items():
            lp_info = info.get("license_plate", {})
            writer.writerow(
                [
                    tid,
                    info.get("vehicle_type", "unknown"),
                    _bbox_to_str(info.get("vehicle_bbox", [])),
                    _bbox_to_str(lp_info.get("bbox", [])),
                    round(lp_info.get("bbox_score", 0.0), 4),
                    info.get("frame_start", -1),
                    info.get("frame_end", -1),
                ]
            )
    print(f"[INFO] CSV results saved → {csv_path}")


def write_json(objects_data: Mapping[int, Dict[str, Any]], json_path: str) -> None:
    """Зберігає результати у JSON із підсумковою статистикою."""
    objects_data = {int(k): v for k, v in objects_data.items()}

    summary: Dict[str, int] = {}
    for obj in objects_data.values():
        vt = obj.get("vehicle_type", "unknown")
        summary[vt] = summary.get(vt, 0) + 1

    to_dump = {"summary": summary, "objects": objects_data}
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(to_dump, fh, indent=2, ensure_ascii=False)
    print(f"[INFO] JSON results saved → {json_path}")
