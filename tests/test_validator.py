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
