import json
import pytest

from flight_analyzer.loader import load_data


def test_load_data_success(tmp_path):
    """
    Test that valid JSON telemetry data loads correctly.
    """

    test_file = tmp_path / "test_flight.json"

    sample_data = [
        {
            "time": 0,
            "altitude": 1000,
            "airspeed": 120,
        }
    ]

    with test_file.open("w", encoding="utf-8") as file:
        json.dump(sample_data, file)

    result = load_data("test_flight.json", data_dir=tmp_path)

    assert result == sample_data


def test_load_data_file_not_found(tmp_path):
    """
    Test that missing files raise the correct error.
    """

    with pytest.raises(FileNotFoundError):
        load_data("does_not_exist.json", data_dir=tmp_path)


def test_load_data_invalid_json(tmp_path):
    """
    Test that malformed JSON raises a ValueError.
    """

    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(ValueError):
        load_data("bad.json", data_dir=tmp_path)


@pytest.mark.parametrize("payload", [None, {}, {"time": 0}, "flight", 42, True])
def test_load_data_rejects_non_list_root(tmp_path, payload):
    (tmp_path / "flight.json").write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="JSON array of telemetry records"):
        load_data("flight.json", data_dir=tmp_path)


@pytest.mark.parametrize("record", [None, [], "flight", 42, True])
def test_load_data_reports_non_object_record_position(tmp_path, record):
    payload = [{"time": 0}, record]
    (tmp_path / "flight.json").write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="record 2 must be a JSON object"):
        load_data("flight.json", data_dir=tmp_path)


def test_load_data_rejects_empty_array(tmp_path):
    (tmp_path / "flight.json").write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="at least one telemetry record"):
        load_data("flight.json", data_dir=tmp_path)
