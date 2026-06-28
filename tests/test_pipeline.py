from pathlib import Path

from seatmap_svg.pipeline import build_effective_config, run_pipeline


def test_build_effective_config_applies_overrides():
    config = build_effective_config(
        input_path="custom.xlsx",
        sheet="Sheet1",
        scan_range="B2:C3",
        output_path="out.svg",
        report_path="report.json",
    )
    assert config["input"]["file"] == "custom.xlsx"
    assert config["input"]["sheet"] == "Sheet1"
    assert config["input"]["range"] == "B2:C3"
    assert config["output"]["svg"] == "out.svg"
    assert config["output"]["report"] == "report.json"


def test_run_pipeline_reuses_core_steps(monkeypatch, tmp_path):
    input_file = tmp_path / "input.xlsx"
    input_file.write_text("placeholder", encoding="utf-8")
    svg = tmp_path / "seatmap.svg"
    report = tmp_path / "report.json"
    calls = []

    class Parsed:
        unknown_cells = []
        stats = {"total": 0, "normal": 0, "added": 0, "disabled": 0}

    def fake_read_sheet(file, sheet, scan_range):
        calls.append(("read", file, sheet, scan_range))
        return object()

    def fake_parse_sheet(data, config):
        calls.append(("parse", config["input"]["file"]))
        return Parsed()

    def fake_write_svg(data, parsed, config, output):
        calls.append(("svg", output))
        Path(output).write_text("<svg />", encoding="utf-8")

    def fake_write_report(data, parsed, config, output):
        calls.append(("report", output))
        Path(output).write_text("{}", encoding="utf-8")

    monkeypatch.setattr("seatmap_svg.pipeline.read_sheet", fake_read_sheet)
    monkeypatch.setattr("seatmap_svg.pipeline.parse_sheet", fake_parse_sheet)
    monkeypatch.setattr("seatmap_svg.pipeline.write_svg", fake_write_svg)
    monkeypatch.setattr("seatmap_svg.pipeline.write_report", fake_write_report)

    result = run_pipeline(input_path=str(input_file), sheet="S", scan_range="A1:A1", output_path=str(svg), report_path=str(report))

    assert result["svg"] == str(svg)
    assert result["report"] == str(report)
    assert [call[0] for call in calls] == ["read", "parse", "svg", "report"]


def test_gui_module_imports_without_starting_window():
    import seatmap_svg.gui as gui

    assert callable(gui.main)
