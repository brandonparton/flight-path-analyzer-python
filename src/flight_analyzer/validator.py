from itertools import pairwise
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
    Validate non-empty telemetry, finite numbers, coordinates, and time order.

    Record numbers are one-based positions, independent of the DataFrame index.
    Input is checked without sorting, coercing values, or dropping extra columns.

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
            is_number = isinstance(value, Real) and not isinstance(value, bool)
            try:
                valid = is_number and isfinite(value)
            except OverflowError:
                valid = False
            if not valid:
                raise ValueError(
                    f"Telemetry record {row} field '{column}' must be a finite number "
                    "within the supported numeric range"
                )

    for column, lower, upper in [("latitude", -90, 90), ("longitude", -180, 180)]:
        for row, value in enumerate(df[column], start=1):
            if not lower <= value <= upper:
                raise ValueError(
                    f"Telemetry record {row} field '{column}' must be between "
                    f"{lower} and {upper} degrees"
                )

    for row, (previous, current) in enumerate(pairwise(df["time"]), start=2):
        if current <= previous:
            raise ValueError(
                f"Telemetry record {row} field 'time' must be greater than "
                f"record {row - 1} (duplicate or out-of-order timestamp)"
            )
