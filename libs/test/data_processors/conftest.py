from unittest.mock import patch

import pytest


@pytest.fixture
def expected_geo_point():
    return {"coordinates": [102.0, 0.5], "type": "Point"}


@pytest.fixture
def expected_geo_line():
    return {
        "type": "LineString",
        "coordinates": [[10.2, 11.3], [11.3, 12.4], [12.5, 13.2]],
    }


@pytest.fixture
def expected_geo_shape():
    return {
        "type": "Polygon",
        "coordinates": [[[11.2, 20.2], [15.2, 21.3], [15.8, 22.0], [11.2, 20.2]]],
    }


@pytest.fixture
def expected_failed_geo_shape():
    return {"type": "Polygon", "coordinates": [[[]]]}


@pytest.fixture
def footprint_to_geo_shape():
    return [[11.2, 20.2], [15.2, 21.3], [15.8, 22.0], [11.2, 20.2]]


@pytest.fixture
def point():
    return {"Latitude": 0.5, "Longtitude": 102.0}


@pytest.fixture
def footprint_to_geo_line():
    return [[10.2, 11.3], [11.3, 12.4], [12.5, 13.2]]


@pytest.fixture
def failed_footprint():
    return [[11.2, 20.2], [15.2, 21.3], [15.8, 22.0], [11.2, 20.3]]


@pytest.fixture
def date():
    return "19062024Z100100"


@pytest.fixture
def invalid_date():
    return "19062024l100100"


@pytest.fixture
def expected_date():
    return "2024-06-19T10:01:00"


@pytest.fixture
def times_message(date):
    return {"Start_time": date, "End_time": date}


@pytest.fixture
def message(times_message):
    return {"id": "test-id", **times_message}


@pytest.fixture
def message_processed(expected_date):
    return {"id": "test-id", "Start_time": expected_date, "End_time": expected_date}


@pytest.fixture
def times_keys():
    return ["Start_time", "End_time"]


@pytest.fixture
def expected_message_log():
    return "Error: first and last points of the poligon must be the same (it must close itself)."


@pytest.fixture
def expected_error_message_log():
    return f"Error: the date {invalid_date} or date format in process is invalid."


@pytest.fixture
def path():
    return "data_processors.data_process_functions"


@pytest.fixture
def patch_extracting_time_keys(path, times_keys):
    return patch(f"{path}.extracting_time_keys", return_value=times_keys)


@pytest.fixture
def patch_process_date(expected_date, path):
    return patch(f"{path}.process_date", return_value=expected_date)
