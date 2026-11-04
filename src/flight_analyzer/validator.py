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
    Validate that the telemetry DataFrame contains all required columns.

    Raises:
        ValueError: If there are no records or required columns are missing.
    """
    if len(df) == 0:
        raise ValueError("Telemetry data must contain at least one telemetry record")

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        missing_str = ", ".join(sorted(missing))
        raise ValueError(
            f"Telemetry data is missing required columns: {missing_str}"
        )
