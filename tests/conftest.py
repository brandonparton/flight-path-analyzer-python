import pytest


@pytest.fixture
def telemetry_record():
    return {
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
