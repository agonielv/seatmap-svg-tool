from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except ImportError:  # pragma: no cover - runtime dependency message
    yaml = None

DEFAULT_CONFIG: Dict[str, Any] = {
    "app": {"name": "SeatmapSVGTool"},
    "input": {"file": "samples/歌剧院座位图—加座版.xlsx", "sheet": "净版", "range": "A1:AX103"},
    "output": {"svg": "output/seatmap.svg", "report": "output/report.json", "preview_png": "output/preview.png"},
    "seat": {"regex": r"^\d+(?:\+\d+)?$", "width": 28, "height": 20, "gap_x": 4, "gap_y": 4, "radius": 4, "font_size": 9},
    "layout": {"origin_x": 40, "origin_y": 40, "cell_width": 32, "cell_height": 24},
    "style": {"normal_fill": "#f04b5f", "added_fill": "#f28c28", "disabled_fill": "#4b4b4b", "label_fill": "#d9d9d9", "stage_fill": "#6fa8dc", "stroke": "#333333", "text_fill": "#111111"},
    "rules": {"added_seat": {"by_text_regex": r"^\d+\+\d+$"}, "disabled_seat": {"by_fill_keys": ["theme:0"]}, "normal_seat": {"by_default": True}},
    "ignore": {"ranges": ["BB1:BF103"]},
}

def deep_update(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_update(result[key], value)
        else:
            result[key] = value
    return result

def load_config(path: str | None = None) -> Dict[str, Any]:
    if not path:
        return deepcopy(DEFAULT_CONFIG)
    if yaml is None:
        raise SystemExit("PyYAML is required to read config files. Install with: python -m pip install -r requirements.txt")
    with Path(path).open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return deep_update(DEFAULT_CONFIG, data)
