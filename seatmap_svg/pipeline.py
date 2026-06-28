from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, Optional

from .config import load_config, resolve_resource_path
from .excel_reader import read_sheet
from .parser import ParseResult, parse_sheet
from .report import write_report
from .svg_writer import write_svg
from .xlcoords import range_boundaries

LogCallback = Optional[Callable[[str], None]]


def _log(callback: LogCallback, message: str) -> None:
    if callback:
        callback(message)


def build_effective_config(
    config_path: str | None = None,
    input_path: str | None = None,
    sheet: str | None = None,
    scan_range: str | None = None,
    output_path: str | None = None,
    report_path: str | None = None,
) -> Dict[str, Any]:
    """Load YAML/default config and apply CLI/GUI overrides."""
    config = load_config(config_path)
    if input_path:
        config["input"]["file"] = input_path
    if sheet:
        config["input"]["sheet"] = sheet
    if scan_range:
        config["input"]["range"] = scan_range
    if output_path:
        config["output"]["svg"] = output_path
    if report_path:
        config["output"]["report"] = report_path
    return config


def validate_pipeline_inputs(config: Dict[str, Any], config_path: str | None = None) -> None:
    """Raise friendly ValueError/FileNotFoundError exceptions before conversion."""
    if config_path and not resolve_resource_path(config_path).exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    input_file = config["input"].get("file")
    if not input_file:
        raise ValueError("未选择 Excel 文件。")
    if not Path(input_file).exists():
        raise FileNotFoundError(f"Excel 文件不存在: {input_file}")
    try:
        range_boundaries(config["input"].get("range", ""))
    except Exception as exc:
        raise ValueError(f"扫描范围格式错误，请使用类似 A1:Z50 的格式: {config['input'].get('range')}") from exc
    for key, label in [("svg", "SVG 输出路径"), ("report", "JSON 报告路径")]:
        output = config["output"].get(key)
        if not output:
            raise ValueError(f"未设置{label}。")
        parent = Path(output).parent
        if parent and parent != Path(""):
            try:
                parent.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise PermissionError(f"无法创建或写入输出目录: {parent}") from exc


def run_pipeline(
    config_path: str | None = None,
    input_path: str | None = None,
    sheet: str | None = None,
    scan_range: str | None = None,
    output_path: str | None = None,
    report_path: str | None = None,
    log_callback: LogCallback = None,
) -> Dict[str, Any]:
    """Run the Excel -> parsed model -> SVG/report pipeline used by CLI and GUI."""
    _log(log_callback, "正在加载配置")
    config = build_effective_config(config_path, input_path, sheet, scan_range, output_path, report_path)
    validate_pipeline_inputs(config, config_path)

    _log(log_callback, f"正在读取 Excel: {config['input']['file']}")
    data = read_sheet(config["input"]["file"], config["input"].get("sheet"), config["input"]["range"])

    _log(log_callback, "正在解析座位")
    parsed: ParseResult = parse_sheet(data, config)
    if parsed.unknown_cells:
        _log(log_callback, f"提示：发现 {len(parsed.unknown_cells)} 个无法识别但有内容的单元格，详情见报告。")

    _log(log_callback, f"正在生成 SVG: {config['output']['svg']}")
    write_svg(data, parsed, config, config["output"]["svg"])

    _log(log_callback, f"正在生成报告: {config['output']['report']}")
    write_report(data, parsed, config, config["output"]["report"])

    _log(log_callback, "完成")
    return {"config": config, "data": data, "parsed": parsed, "svg": config["output"]["svg"], "report": config["output"]["report"]}
