import json
import logging
import os
from pathlib import Path
import subprocess
import sys

import plotly.graph_objects as go
import pytest

from flight_analyzer.main import main

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def forbid_figures(monkeypatch):
    def unexpected_figure(*args, **kwargs):
        raise AssertionError("Invalid telemetry reached figure construction")

    monkeypatch.setattr(go, "Figure", unexpected_figure)


@pytest.mark.parametrize(
    ("updates", "field"),
    [
        ({"latitude": 91}, "latitude"),
        ({"longitude": -181}, "longitude"),
        ({"time": "0"}, "time"),
        ({"fuel": None}, "fuel"),
        ({"airspeed": True}, "airspeed"),
        ({"altitude": float("inf")}, "altitude"),
    ],
)
def test_invalid_telemetry_fails_before_plotting(
    tmp_path, telemetry_record, monkeypatch, caplog, forbid_figures, updates, field,
):
    path = tmp_path / "flight.json"
    path.write_text(
        json.dumps([{**telemetry_record, **updates}]), encoding="utf-8",
    )
    monkeypatch.setattr(sys, "argv", ["flight-analyzer", str(path)])

    with caplog.at_level(logging.ERROR):
        assert main() == 1

    assert f"record 1 field '{field}'" in caplog.text


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        (None, "JSON array"),
        ({}, "JSON array"),
        ([], "at least one telemetry record"),
        ([None], "record 1 must be a JSON object"),
        ([{}], "missing required columns"),
    ],
)
def test_invalid_structure_fails_before_plotting(
    tmp_path, monkeypatch, caplog, forbid_figures, payload, message,
):
    path = tmp_path / "flight.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["flight-analyzer", str(path)])

    with caplog.at_level(logging.ERROR):
        assert main() == 1

    assert message in caplog.text


@pytest.mark.parametrize("times", [[0, 0], [1, 0]])
def test_invalid_time_order_fails_before_plotting(
    tmp_path, telemetry_record, monkeypatch, caplog, forbid_figures, times,
):
    path = tmp_path / "flight.json"
    records = [{**telemetry_record, "time": time} for time in times]
    path.write_text(json.dumps(records), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["flight-analyzer", str(path)])

    with caplog.at_level(logging.ERROR):
        assert main() == 1

    assert "record 2 field 'time'" in caplog.text


@pytest.mark.parametrize(
    ("contents", "message"),
    [("null", "JSON array of telemetry records"), ("{invalid", "Invalid JSON")],
)
def test_module_exits_nonzero_for_invalid_input(tmp_path, contents, message):
    path = tmp_path / "flight.json"
    path.write_text(contents, encoding="utf-8")
    env = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "src")}

    result = subprocess.run(
        [sys.executable, "-m", "flight_analyzer.main", str(path)],
        cwd=tmp_path, env=env, capture_output=True, text=True, timeout=30,
    )

    assert result.returncode == 1
    assert message in result.stderr
    assert "Traceback" not in result.stderr


def test_missing_file_returns_failure(tmp_path, monkeypatch, caplog, forbid_figures):
    monkeypatch.setattr(
        sys, "argv", ["flight-analyzer", str(tmp_path / "missing.json")],
    )

    with caplog.at_level(logging.ERROR):
        assert main() == 1

    assert "Telemetry file not found" in caplog.text


@pytest.mark.parametrize("sample", ["repository", "single_record"])
def test_valid_input_keeps_both_visualizations(
    tmp_path, telemetry_record, monkeypatch, sample,
):
    if sample == "repository":
        path = PROJECT_ROOT / "data" / "flight_data.json"
    else:
        path = tmp_path / "flight.json"
        path.write_text(json.dumps([telemetry_record]), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["flight-analyzer", str(path)])
    figures = []
    monkeypatch.setattr(go.Figure, "show", lambda self: figures.append(self))

    assert main() == 0
    assert len(figures) == 2


def test_plot_errors_are_not_misreported_as_input_errors(monkeypatch):
    path = PROJECT_ROOT / "data" / "flight_data.json"
    monkeypatch.setattr(sys, "argv", ["flight-analyzer", str(path)])

    def failed_display(self):
        raise ValueError("display failed")

    monkeypatch.setattr(go.Figure, "show", failed_display)

    with pytest.raises(ValueError, match="display failed"):
        main()
