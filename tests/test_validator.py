import pandas as pd
import pytest

from flight_analyzer.validator import validate_dataframe


def test_valid_dataframe():

    df = pd.DataFrame(
        [
            {
                "time": 0,
                "altitude": 1000,
                "airspeed": 120,
                "pitch": 1,
                "roll": 2,
                "throttle": 50,
                "fuel": 90,
                "latitude": 35.5,
                "longitude": -86.6,
            }
        ]
    )

    validate_dataframe(df)


def test_missing_columns():

    df = pd.DataFrame(
        [
            {
                "time": 0,
                "altitude": 1000,
            }
        ]
    )

    with pytest.raises(ValueError):
        validate_dataframe(df)


@pytest.mark.parametrize(
    "columns",
    [
        [],
        ["time", "altitude", "airspeed", "pitch", "roll", "throttle", "fuel",
         "latitude", "longitude"],
    ],
)
def test_empty_dataframe_is_rejected(columns):
    with pytest.raises(ValueError, match="at least one telemetry record"):
        validate_dataframe(pd.DataFrame(columns=columns))


@pytest.mark.parametrize(
    "field",
    ["time", "altitude", "airspeed", "pitch", "roll", "throttle", "fuel",
     "latitude", "longitude"],
)
@pytest.mark.parametrize(
    "value",
    [None, "100", True, False, float("nan"), float("inf"), -float("inf")],
)
def test_required_values_must_be_finite_numbers(telemetry_record, field, value):
    second = {**telemetry_record, "time": 1, field: value}
    df = pd.DataFrame([telemetry_record, second], index=[10, 20])

    with pytest.raises(ValueError, match=rf"record 2 field '{field}'.*finite number"):
        validate_dataframe(df)


@pytest.mark.parametrize("value", ["bad", [], {}, 1 + 2j, pd.NA])
def test_non_real_values_are_rejected(telemetry_record, value):
    record = {**telemetry_record, "altitude": value}
    with pytest.raises(ValueError, match="record 1 field 'altitude'.*finite number"):
        validate_dataframe(pd.DataFrame([record]))


def test_missing_value_in_one_record_reports_its_position(telemetry_record):
    second = {**telemetry_record, "time": 1}
    del second["fuel"]

    with pytest.raises(ValueError, match="record 2 field 'fuel'.*finite number"):
        validate_dataframe(pd.DataFrame([telemetry_record, second]))


def test_extra_columns_and_finite_values_are_preserved(telemetry_record):
    record = {
        **telemetry_record, "time": 0.5, "altitude": -20.5, "fuel": 101.0,
        "yaw": "unvalidated extra", "note": None,
    }
    df = pd.DataFrame([record])
    original = df.copy(deep=True)

    validate_dataframe(df)

    pd.testing.assert_frame_equal(df, original)


@pytest.mark.parametrize(
    ("field", "value", "bounds"),
    [
        ("latitude", -90.01, "-90 and 90"),
        ("latitude", 90.01, "-90 and 90"),
        ("longitude", -180.01, "-180 and 180"),
        ("longitude", 180.01, "-180 and 180"),
    ],
)
def test_coordinates_outside_bounds_are_rejected(telemetry_record, field, value, bounds):
    second = {**telemetry_record, "time": 1, field: value}
    with pytest.raises(ValueError, match=rf"record 2 field '{field}'.*{bounds}"):
        validate_dataframe(pd.DataFrame([telemetry_record, second]))


@pytest.mark.parametrize("latitude", [-90, 0, 90])
@pytest.mark.parametrize("longitude", [-180, 0, 180])
def test_coordinate_boundaries_are_inclusive(telemetry_record, latitude, longitude):
    record = {**telemetry_record, "latitude": latitude, "longitude": longitude}
    validate_dataframe(pd.DataFrame([record]))


@pytest.mark.parametrize(
    ("times", "row"),
    [([0, 0], 2), ([1, 0], 2), ([0, 2, 1], 3), ([0, 1, 1], 3)],
)
def test_times_must_strictly_increase_in_input_order(telemetry_record, times, row):
    df = pd.DataFrame([{**telemetry_record, "time": time} for time in times])
    with pytest.raises(ValueError, match=rf"record {row} field 'time'.*greater than"):
        validate_dataframe(df)


@pytest.mark.parametrize("times", [[42], [-5, -1, 0], [0.25, 1, 60.5]])
def test_single_and_irregular_increasing_times_are_valid(telemetry_record, times):
    df = pd.DataFrame([{**telemetry_record, "time": time} for time in times])
    original = df.copy(deep=True)

    validate_dataframe(df)

    pd.testing.assert_frame_equal(df, original)
