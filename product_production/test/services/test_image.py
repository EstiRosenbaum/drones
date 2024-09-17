import json
from unittest.mock import patch

import pytest


@pytest.fixture
def Sensor_Position():
    return {"Latitude": 32.113225, "Longtitude": 34.786673}


@pytest.fixture
def basic_message():
    return {
        "image_id": "TEST_19062024_100011_0011",
        "Platform_name": "PlatformA",
        "Sensor_type": "SensorB",
        "Platform_id": "PlatformA123",
        "Sensor_id": "SensorB123",
        "Sortie_id": "SortieB123",
        "Sensor_Orientation": {"Pitch": -90, "Roll": 0, "Yaw": 270},
    }


@pytest.fixture
def unprocessed_date():
    return "19062024Z100100"


@pytest.fixture
def geo_point_process():
    return {
        "coordinates": [34.786673, 32.113225],
        "type": "Point",
    }


@pytest.fixture
def times_message(unprocessed_date):
    return {
        "Photo_time": unprocessed_date,
        "Landing_time": unprocessed_date,
        "Start_Production_time": unprocessed_date,
        "End_Production_time": unprocessed_date,
    }


@pytest.fixture
def times_processed(date):
    return {
        "Photo_time": date,
        "Landing_time": date,
        "Start_Production_time": date,
        "End_Production_time": date,
    }


@pytest.fixture
def message(Sensor_Position, times_message, basic_message):
    return json.dumps(
        {
            "Sensor_Position": Sensor_Position,
            **times_message,
            **basic_message,
        }
    )


@pytest.fixture
def message_with_date_processed(Sensor_Position, basic_message, times_processed):
    return {
        "Sensor_Position": Sensor_Position,
        "Sensor_Orientation": {"Pitch": -90, "Roll": 0, "Yaw": 270},
        **basic_message,
        **times_processed,
    }


@pytest.fixture
def message_processed(geo_point_process, basic_message, times_processed):
    return {
        "Sensor_Position": geo_point_process,
        "Sensor_Orientation": {"Pitch": -90, "Roll": 0, "Yaw": 270},
        **basic_message,
        **times_processed,
    }


@pytest.fixture
def current_path():
    return "services.image"


@pytest.fixture
def class_path(current_path):
    return f"{current_path}.Image"


@pytest.fixture
def patch_process_geo_point(geo_point_process, current_path):
    return patch(
        f"{current_path}.process_geo_point",
        return_value=geo_point_process,
    )


@pytest.fixture
def patch_process_dates(message_with_date_processed, current_path):
    return patch(
        f"{current_path}.process_dates",
        return_value=message_with_date_processed,
    )


def test_process_message(
    image,
    message,
    message_processed,
    Sensor_Position,
    patch_process_dates,
    patch_process_geo_point,
):
    with patch_process_dates as process_dates, patch_process_geo_point as process_geo_point:
        new_message_processor = image._process_message(message)
        assert new_message_processor == message_processed
        process_dates.assert_called_with(json.loads(message))
        process_geo_point.assert_called_with(Sensor_Position)


def test_post_process_message(
    image,
    date,
    message_processed,
    times_message,
    patch_extracting_time_properties,
    patch_update_message,
):
    from utils.const import Indexes

    with patch_extracting_time_properties as extracting_time_properties, patch_update_message as _update_message:
        image._post_process_message(message_processed)
        extracting_time_properties.assert_called_once_with(message_processed)
        _update_message.assert_called_once_with(
            times_message, Indexes.DATES, {"Photo_time": date}
        )
