# Flight Path Analyzer

Flight Path Analyzer is a Python-based telemetry visualization application that analyzes simulated aircraft flight data. It generates an interactive 3D flight path from takeoff to landing alongside telemetry dashboards for altitude, airspeed, pitch, roll, throttle, and fuel remaining.

## Features

### Interactive Visualizations
- **3D Flight Path**
  - Displays aircraft trajectory using latitude, longitude, and altitude.
  - Color mapping shows altitude changes throughout the flight.
  - Highlights takeoff and landing points.

- **Telemetry Dashboard**
  - Altitude profile
  - Airspeed changes
  - Pitch and roll attitude
  - Throttle usage
  - Fuel remaining

### Application Architecture
- Modular Python package structure
- JSON telemetry loading
- Input data validation
- Automated tests with pytest
- Package installation

## Version History

### v2.0.0
Rebuilt the whole thing as a proper installable package instead of one big script. Split the logic into separate modules: loader, validator, charts, flight path.

Also added:
- Validation that checks for required columns before anything tries to chart
- Error handling for missing files and bad JSON (v1 just crashed)
- Takeoff/landing markers on the 3D flight path
- A pytest suite
- Logging instead of print statements
- pyproject.toml packaging


### v1.0.0
One script, hardcoded to load `flight_data.json`, no tests, no validation. Generated the 3D flight path and the telemetry charts but the 3D path was just the trajectory line, no start/end markers.

## Installation

Clone the repository:

```bash
git clone https://github.com/brandonparton/flight-path-analyzer-python.git
cd flight-path-analyzer-python
```

Install the project:

```bash
pip install -e .
```

Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

Run the application:

```bash
flight-analyzer flight_data.json
```

The application will:

1. Load telemetry data
2. Validate record structure, numeric values, coordinates, and time order
3. Generate a 3D flight path visualization
4. Display telemetry charts

For the current editable installation, relative filenames are resolved inside
the repository's `data/` directory. An absolute path can be used for another
file. Installed-wheel sample handling is tracked separately in
[issue #10](https://github.com/brandonparton/flight-path-analyzer-python/issues/10).

## Telemetry Input Contract

Input must be a non-empty JSON array of objects. Every record must supply these
fields as finite JSON numbers within the supported numeric range:

| Field | Unit / meaning | Validation |
| --- | --- | --- |
| `time` | Seconds relative to a consistent recording origin | Strictly increasing in input order |
| `altitude` | Feet, using the source's altitude reference | Finite number |
| `airspeed` | Knots, as supplied by the source | Finite number |
| `pitch`, `roll` | Degrees | Finite numbers |
| `throttle` | Percent | Finite number |
| `fuel` | Fuel remaining, percent | Finite number |
| `latitude` | Decimal degrees | -90 through 90, inclusive |
| `longitude` | Decimal degrees | -180 through 180, inclusive |

- A single record is valid. Irregular sampling is allowed; timestamps need not
  start at zero and may use a negative offset.
- Duplicate or decreasing timestamps are rejected. Records are not silently
  sorted, removed, or interpolated.
- Numeric strings such as `"120"`, booleans, null/missing required values,
  NaN, infinity, and numbers too large for the finite-number check are rejected.
- Extra fields, such as the sample's `yaw`, are retained but not validated or
  used by the current plots.
- The sample does not declare an altitude datum such as mean sea level or height
  above ground. Supply a consistent reference; validation does not infer one,
  require altitude to be nonnegative, or detect takeoff/landing.
- Fuel is a remaining-percentage reading, not fuel mass or consumption rate.
  No additional physical limits are imposed on altitude, airspeed, attitude,
  throttle, or fuel until a source-specific contract establishes them.

Minimal valid example:

```json
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
    "longitude": -86.6
  }
]
```

Invalid input exits with status `1` before any figure is created. Expected file
and validation errors are reported without a traceback, for example:

```text
ERROR: Telemetry record 2 field 'latitude' must be between -90 and 90 degrees
```

Record numbers are one-based positions in the input, not JSON file line numbers.
Successful analysis exits with status `0`; unexpected plotting failures are
allowed to propagate for diagnosis.

## Running Tests

Run the test suite:

```bash
python -m pytest
```

Tests cover loader structure, required values, coordinate boundaries, time
ordering, CLI errors, and the valid sample/single-record workflows. CLI tests
intercept Plotly display so they do not open browser windows; they do not verify
interactive browser rendering.

## Project Structure

```
flight-path-analyzer-python/
├── data/
│   └── flight_data.json
│
├── src/
│   └── flight_analyzer/
│       ├── main.py
│       ├── loader.py
│       ├── validator.py
│       ├── charts.py
│       └── flight_path.py
│
├── tests/
│   ├── conftest.py
│   ├── test_loader.py
│   ├── test_main.py
│   └── test_validator.py
│
├── pyproject.toml
└── README.md
```

## Example Output

Telemetry Dashboard

![Flight Telemetry Example](images/telemetry_example.png)

3D Flight Path

![3D Flight Path Example](images/3d_example.png)

## Technologies

- Python 3.11+
- Pandas
- Plotly
- Pytest
- JSON Data Processing
