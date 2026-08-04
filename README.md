# Flight Path Analyzer

Flight Path Analyzer is a Python-based telemetry visualization application that analyzes simulated aircraft flight data. It generates an interactive 3D flight path from takeoff to landing alongside telemetry dashboards for altitude, airspeed, pitch, roll, throttle, and fuel consumption.

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
  - Fuel consumption

### Application Architecture
- Modular Python package structure
- JSON telemetry loading
- Input data validation
- Command-line interface
- Automated tests with pytest
- Editable package installation

## Version History

### v2.0.0
Rebuilt the whole thing as a proper installable package instead of one big script. Split the logic into separate modules (loader, validator, charts, flight path) and added a real CLI so you can point it at any telemetry file instead of editing the filename in code.

Also added:
- Validation that checks for required columns before anything tries to chart
- Actual error handling for missing files and bad JSON (v1 just crashed)
- Takeoff/landing markers on the 3D flight path
- A pytest suite
- Logging instead of print statements
- pyproject.toml packaging, so it installs with pip

Also cleaned up the chart code — it was six nearly-identical blocks for each telemetry line, now it's driven off a small config list.

### v1.0.0
First version. One script, hardcoded to load `flight_data.json`, no tests, no validation. Generated the 3D flight path and the telemetry charts but the 3D path was just the trajectory line, no start/end markers.

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/flight-path-analyzer-python.git
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

Place your telemetry JSON file in the `data/` directory, then run the flight analyzer:

```bash
flight-analyzer flight_data.json
```

The application will:

1. Load telemetry data
2. Validate required fields
3. Generate a 3D flight path visualization
4. Display telemetry charts

## Running Tests

Run the test suite:

```bash
pytest
```

Expected output:

```
5 passed
```

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
│   ├── test_loader.py
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

## Roadmap

- Add a flight summary report (duration, max altitude, max speed, fuel used)
- Add screenshots/GIFs of the actual v2 output
