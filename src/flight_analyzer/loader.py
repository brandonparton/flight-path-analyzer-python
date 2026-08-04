from pathlib import Path
import json
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_data(filename: str, data_dir: Path = DATA_DIR) -> list[dict[str, Any]]:
    """
    Load flight telemetry data from a JSON file.

    Args:
        filename: Name of the JSON file located in the data directory.
        data_dir: Directory to look for the file in. Defaults to the
            package's DATA_DIR. Override in tests to point at a temp dir.

    Returns:
        A list of dictionaries containing telemetry records.

    Raises:
        FileNotFoundError: If the file cannot be found.
        ValueError: If the JSON is invalid.
    """
    file_path = data_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Telemetry file not found: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in '{filename}': {e}") from e