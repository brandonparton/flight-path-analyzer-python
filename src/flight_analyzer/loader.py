from pathlib import Path
import json
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_data(filename: str, data_dir: Path = DATA_DIR) -> list[dict[str, Any]]:
    """
    Load a non-empty JSON array of telemetry objects.

    Args:
        filename: Name of the JSON file located in the data directory.
        data_dir: Directory to look for the file in. Defaults to the
            package's DATA_DIR. Override in tests to point at a temp dir.

    Returns:
        A list of dictionaries containing telemetry records.

    Raises:
        FileNotFoundError: If the file cannot be found.
        ValueError: If the JSON is invalid, empty, or not an array of objects.
    """
    file_path = data_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Telemetry file not found: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in '{filename}': {e}") from e

    if not isinstance(data, list):
        raise ValueError("Telemetry data must be a JSON array of telemetry records")

    if not data:
        raise ValueError("Telemetry data must contain at least one telemetry record")

    for row, record in enumerate(data, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Telemetry record {row} must be a JSON object")

    return data
