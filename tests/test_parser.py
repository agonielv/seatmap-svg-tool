from seatmap_svg.config import DEFAULT_CONFIG
from seatmap_svg.excel_reader import CellInfo, SheetData
from seatmap_svg.parser import parse_sheet

def test_parser_detects_normal_and_added():
    cells = [
        CellInfo(1, 1, "A1", "1排", "none", None, False, None, None),
        CellInfo(1, 2, "B1", "12", "none", None, False, None, None),
        CellInfo(1, 3, "C1", "12+1", "none", None, False, None, None),
    ]
    data = SheetData("x.xlsx", "S", "A1:C1", 1, 1, 3, 1, cells, [])
    parsed = parse_sheet(data, DEFAULT_CONFIG)
    assert parsed.stats["normal"] == 1
    assert parsed.stats["added"] == 1
    assert parsed.stats["total"] == 2
