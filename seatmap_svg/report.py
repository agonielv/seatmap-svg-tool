from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .excel_reader import SheetData
from .parser import ParseResult

def write_report(data: SheetData, parsed: ParseResult, config: Dict[str, Any], output: str) -> None:
    report = {
        "input": {"file": data.file, "sheet": data.sheet, "range": data.scan_range},
        "output": config.get("output", {}),
        "seat_statistics": {
            "total_seats": parsed.stats["total"],
            "normal_seats": parsed.stats["normal"],
            "added_seats": parsed.stats["added"],
            "disabled_seats": parsed.stats["disabled"],
            "label_blocks": parsed.stats["labels"],
        },
        "ignored_cell_count": parsed.ignored_count,
        "unrecognized_non_empty_cells": parsed.unknown_cells,
        "fill_color_counts": parsed.fill_counts,
        "merged_ranges": data.merged_ranges,
        "notes": ["统计区可通过 ignore.ranges 排除。", "主题色会以 theme:N 形式输出，可复制到 rules.disabled_seat.by_fill_keys 等规则中。"],
    }
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
