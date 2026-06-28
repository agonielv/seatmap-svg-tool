from __future__ import annotations

import argparse
from .pipeline import run_pipeline


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
    result = run_pipeline(
        config_path=args.config,
        input_path=args.input,
        sheet=args.sheet,
        scan_range=args.scan_range,
        output_path=args.output,
        report_path=args.report,
        log_callback=print,
    )
    parsed = result["parsed"]
    print(f"SVG written: {result['svg']}")
    print(f"Report written: {result['report']}")
    print(f"Seats: {parsed.stats['total']} (normal={parsed.stats['normal']}, added={parsed.stats['added']}, disabled={parsed.stats['disabled']})")
    return 0
