from math import isfinite
from numbers import Real

from pandas import DataFrame

REQUIRED_COLUMNS = {
    "time",
    "altitude",
    "airspeed",
    "pitch",
    "roll",
    "throttle",
    "fuel",
    "latitude",
    "longitude",
}


def validate_dataframe(df: DataFrame) -> None:
    """
    Validate non-empty telemetry, finite numbers, and geographic coordinates.

    Raises:
        ValueError: If records, required columns, or numeric values are invalid.
    """
    if len(df) == 0:
        raise ValueError("Telemetry data must contain at least one telemetry record")

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        missing_str = ", ".join(sorted(missing))
        raise ValueError(
            f"Telemetry data is missing required columns: {missing_str}"
        )

    for column in sorted(REQUIRED_COLUMNS):
        for row, value in enumerate(df[column], start=1):
            if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(value):
                raise ValueError(
                    f"Telemetry record {row} field '{column}' must be a finite number"
                )

    for column, lower, upper in [("latitude", -90, 90), ("longitude", -180, 180)]:
        for row, value in enumerate(df[column], start=1):
            if not lower <= value <= upper:
                raise ValueError(
                    f"Telemetry record {row} field '{column}' must be between "
                    f"{lower} and {upper} degrees"
                )
