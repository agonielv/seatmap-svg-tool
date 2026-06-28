from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Dict

from .excel_reader import SheetData
from .parser import ParseResult, Element

def _pos(el: Element, data: SheetData, config: Dict[str, Any]):
    layout = config["layout"]
    x = layout["origin_x"] + (el.cell.col - data.min_col) * layout["cell_width"]
    y = layout["origin_y"] + (el.cell.row - data.min_row) * layout["cell_height"]
    return x, y

def write_svg(data: SheetData, parsed: ParseResult, config: Dict[str, Any], output: str) -> None:
    seat = config["seat"]; layout = config["layout"]; style = config["style"]
    width = layout["origin_x"] * 2 + (data.max_col - data.min_col + 1) * layout["cell_width"]
    height = layout["origin_y"] * 2 + (data.max_row - data.min_row + 1) * layout["cell_height"]
    css = f""".seat rect{{stroke:{style['stroke']};stroke-width:1}} .seat-normal rect{{fill:{style['normal_fill']}}} .seat-added rect{{fill:{style['added_fill']}}} .seat-disabled rect{{fill:{style['disabled_fill']}}} .label rect{{fill:{style['label_fill']};stroke:{style['stroke']};stroke-width:.5;opacity:.72}} .stage rect{{fill:{style['stage_fill']};stroke:{style['stroke']};stroke-width:1}} text{{font-family:'Microsoft YaHei','SimHei',Arial,sans-serif;fill:{style['text_fill']};dominant-baseline:middle;text-anchor:middle}} .seat text{{font-size:{seat['font_size']}px}} .label text,.stage text{{font-size:12px;font-weight:600}}"""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<title>Seatmap SVG Tool Output</title>', f'<style>{css}</style>', '<g id="excel-seatmap">']
    for el in parsed.elements:
        x, y = _pos(el, data, config)
        if el.kind == "seat":
            rx = seat.get("radius", 4)
            rect_x = x + (layout["cell_width"] - seat["width"]) / 2
            rect_y = y + (layout["cell_height"] - seat["height"]) / 2
            cls = f"seat seat-{el.status}"
            parts.append(f'<g class="{cls}" data-cell="{el.cell.coordinate}" data-row-label="{escape(el.row_label)}" data-seat="{escape(el.text)}" data-status="{el.status}"><rect x="{rect_x:.2f}" y="{rect_y:.2f}" width="{seat["width"]}" height="{seat["height"]}" rx="{rx}"/><text x="{x + layout["cell_width"]/2:.2f}" y="{y + layout["cell_height"]/2 + 1:.2f}">{escape(el.text)}</text></g>')
        else:
            colspan = rowspan = 1
            if el.cell.merge_bounds:
                min_col, min_row, max_col, max_row = el.cell.merge_bounds
                colspan = max_col - min_col + 1; rowspan = max_row - min_row + 1
            w = layout["cell_width"] * colspan - 2; h = layout["cell_height"] * rowspan - 2
            parts.append(f'<g class="{el.kind}" data-cell="{el.cell.coordinate}" data-text="{escape(el.text)}"><rect x="{x+1:.2f}" y="{y+1:.2f}" width="{w:.2f}" height="{h:.2f}" rx="3"/><text x="{x+w/2:.2f}" y="{y+h/2:.2f}">{escape(el.text)}</text></g>')
    parts += ['</g>', '</svg>']
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text("\n".join(parts), encoding="utf-8")
