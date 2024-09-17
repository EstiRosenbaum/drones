import pytest


@pytest.fixture
def message():
    import json

    return json.dumps(
        {
            "rout_id": "routD",
            "Date": "22062024Z073021",
            "Waypoints": [
                [30.113230, 12.786673],
                [30.113240, 12.786673],
                [30.113250, 12.786673],
            ],
            "Priority": 2,
        }
    )


@pytest.fixture
def message_processed():
    return {
        "rout_id": "routD",
        "Date": "2024-06-22T07:30:21",
        "Waypoints": {
            "type": "LineString",
            "coordinates": [
                [30.113230, 12.786673],
                [30.113240, 12.786673],
                [30.113250, 12.786673],
            ],
        },
        "Priority": 2,
    }


def test_process_message(flight_route, message, message_processed):
    new_message_processor = flight_route._process_message(message)
    assert new_message_processor == message_processed
