from pathlib import Path
from seatmap_svg.config import DEFAULT_CONFIG
from seatmap_svg.excel_reader import CellInfo, SheetData
from seatmap_svg.parser import parse_sheet
from seatmap_svg.svg_writer import write_svg

def test_svg_contains_data_attributes(tmp_path):
    cells = [CellInfo(1, 1, "A1", "8+1", "none", None, False, None, None)]
    data = SheetData("x.xlsx", "S", "A1:A1", 1, 1, 1, 1, cells, [])
    parsed = parse_sheet(data, DEFAULT_CONFIG)
    out = tmp_path / "seatmap.svg"
    write_svg(data, parsed, DEFAULT_CONFIG, str(out))
    text = out.read_text(encoding="utf-8")
    assert 'data-cell="A1"' in text
    assert 'data-status="added"' in text
