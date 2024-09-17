import pytest


@pytest.fixture
def message():
    import json

    return json.dumps(
        {
            "Area_id": "Area128",
            "Date": "22062024Z073021",
            "Platform_needed": ["Pa", "Pb"],
            "Footprint": [
                [22.113225, 34.786673],
                [32.113225, 34.786673],
                [32.113225, 22.786673],
                [32.113225, 22.786673],
                [22.113225, 34.786673],
            ],
            "Priority": 3,
        },
    )


@pytest.fixture
def message_processed():
    return {
        "Area_id": "Area128",
        "Date": "2024-06-22T07:30:21",
        "Platform_needed": ["Pa", "Pb"],
        "Footprint": {
            "type": "Polygon",
            "coordinates": [
                [
                    [22.113225, 34.786673],
                    [32.113225, 34.786673],
                    [32.113225, 22.786673],
                    [32.113225, 22.786673],
                    [22.113225, 34.786673],
                ]
            ],
        },
        "Priority": 3,
    }


def test_process_message(area_photography_request, message, message_processed):
    new_message_processor = area_photography_request._process_message(message)
    assert new_message_processor == message_processed
