from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Set

from .xlcoords import range_boundaries
from .excel_reader import CellInfo, SheetData

@dataclass
class Element:
    kind: str
    cell: CellInfo
    text: str
    status: str = "label"
    row_label: str = ""

@dataclass
class ParseResult:
    elements: List[Element]
    ignored_count: int
    unknown_cells: List[Dict[str, str]]
    fill_counts: Dict[str, int]
    stats: Dict[str, int]

def _in_ranges(cell: CellInfo, ranges: List[str]) -> bool:
    for r in ranges:
        min_col, min_row, max_col, max_row = range_boundaries(r)
        if min_row <= cell.row <= max_row and min_col <= cell.col <= max_col:
            return True
    return False

def parse_sheet(data: SheetData, config: Dict[str, Any]) -> ParseResult:
    seat_re = re.compile(config["seat"].get("regex", r"^\d+(?:\+\d+)?$"))
    added_re = re.compile(config["rules"].get("added_seat", {}).get("by_text_regex", r"^\d+\+\d+$"))
    disabled_fills: Set[str] = set(config["rules"].get("disabled_seat", {}).get("by_fill_keys", []))
    ignore_ranges = config.get("ignore", {}).get("ranges", []) or []
    elements: List[Element] = []
    unknown: List[Dict[str, str]] = []
    fill_counts: Dict[str, int] = {}
    ignored = 0
    stats = {"total": 0, "normal": 0, "added": 0, "disabled": 0, "labels": 0}
    row_labels: Dict[int, str] = {}
    emitted_merges: Set[str] = set()

    for cell in data.cells:
        if _in_ranges(cell, ignore_ranges):
            ignored += 1
            continue
        fill_counts[cell.fill_key] = fill_counts.get(cell.fill_key, 0) + 1
        text = cell.value
        if not text:
            continue
        if re.search(r"排$", text) or re.search(r"^第?.+排$", text):
            row_labels[cell.row] = text
        if seat_re.match(text):
            status = "disabled" if cell.fill_key in disabled_fills else ("added" if added_re.match(text) else "normal")
            elements.append(Element("seat", cell, text, status, row_labels.get(cell.row, "")))
            stats["total"] += 1; stats[status] += 1
            continue
        if cell.is_merged:
            if cell.merge_range in emitted_merges:
                continue
            emitted_merges.add(cell.merge_range or cell.coordinate)
        kind = "stage" if any(k in text for k in ["舞台", "台口", "STAGE", "Stage"]) else "label"
        elements.append(Element(kind, cell, text, kind))
        stats["labels"] += 1
        # Long numeric/statistical text is useful in report but not an error; keep concise unknown list.
        if len(text) <= 40 and not cell.is_merged and kind == "label":
            unknown.append({"cell": cell.coordinate, "text": text, "fill": cell.fill_key})
    return ParseResult(elements, ignored, unknown, fill_counts, stats)
