import pytest


@pytest.fixture
def message():
    import json

    return json.dumps(
        {
            "Location_id": "location129",
            "Date": "12122023Z232556",
            "Platform_needed": ["Pa", "Pb"],
            "Footprint": [
                [15.458565, 81.455654],
                [15.569874, 81.657895],
                [15.865423, 81.945213],
                [15.654123, 81.541335],
                [15.458565, 81.455654],
            ],
            "Priority": 3,
        }
    )


@pytest.fixture
def message_processed():
    return {
        "Location_id": "location129",
        "Date": "2023-12-12T23:25:56",
        "Platform_needed": ["Pa", "Pb"],
        "Footprint": {
            "type": "Polygon",
            "coordinates": [
                [
                    [15.458565, 81.455654],
                    [15.569874, 81.657895],
                    [15.865423, 81.945213],
                    [15.654123, 81.541335],
                    [15.458565, 81.455654],
                ]
            ],
        },
        "Priority": 3,
    }


def test_process_message(location_photography_request, message, message_processed):
    new_message_processor = location_photography_request._process_message(message)
    assert new_message_processor == message_processed
