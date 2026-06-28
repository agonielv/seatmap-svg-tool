from __future__ import annotations
import re

def column_index_from_string(col: str) -> int:
    total = 0
    for ch in col.upper():
        total = total * 26 + (ord(ch) - ord('A') + 1)
    return total

def get_column_letter(idx: int) -> str:
    letters = ''
    while idx:
        idx, rem = divmod(idx - 1, 26)
        letters = chr(65 + rem) + letters
    return letters

def coordinate_to_tuple(coord: str) -> tuple[int, int]:
    m = re.match(r"^([A-Z]+)(\d+)$", coord.upper())
    if not m:
        raise ValueError(f"Invalid coordinate: {coord}")
    return int(m.group(2)), column_index_from_string(m.group(1))

def range_boundaries(rng: str) -> tuple[int, int, int, int]:
    if ':' not in rng:
        row, col = coordinate_to_tuple(rng)
        return col, row, col, row
    start, end = rng.split(':', 1)
    row1, col1 = coordinate_to_tuple(start)
    row2, col2 = coordinate_to_tuple(end)
    return min(col1, col2), min(row1, row2), max(col1, col2), max(row1, row2)
