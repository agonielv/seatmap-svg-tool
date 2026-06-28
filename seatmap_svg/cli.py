from __future__ import annotations

import argparse
from .config import load_config
from .excel_reader import read_sheet
from .parser import parse_sheet
from .svg_writer import write_svg
from .report import write_report

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate an SVG seatmap from an Excel worksheet.")
    p.add_argument("--config", help="YAML config path")
    p.add_argument("--input", help="Excel file path")
    p.add_argument("--sheet", help="Worksheet name")
    p.add_argument("--range", dest="scan_range", help="Scan range, e.g. A1:AX103")
    p.add_argument("--output", help="Output SVG path")
    p.add_argument("--report", help="Output report JSON path")
    return p

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    if args.input: config["input"]["file"] = args.input
    if args.sheet: config["input"]["sheet"] = args.sheet
    if args.scan_range: config["input"]["range"] = args.scan_range
    if args.output: config["output"]["svg"] = args.output
    if args.report: config["output"]["report"] = args.report
    data = read_sheet(config["input"]["file"], config["input"].get("sheet"), config["input"]["range"])
    parsed = parse_sheet(data, config)
    write_svg(data, parsed, config, config["output"]["svg"])
    write_report(data, parsed, config, config["output"]["report"])
    print(f"SVG written: {config['output']['svg']}")
    print(f"Report written: {config['output']['report']}")
    print(f"Seats: {parsed.stats['total']} (normal={parsed.stats['normal']}, added={parsed.stats['added']}, disabled={parsed.stats['disabled']})")
    return 0
