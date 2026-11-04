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
