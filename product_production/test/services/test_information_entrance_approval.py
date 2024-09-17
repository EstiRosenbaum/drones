import json
from unittest.mock import patch

import pytest


@pytest.fixture
def message():
    return json.dumps(
        {
            "image_id": "TEST_19062024_100010_0000",
            "Photo_time": "19062024Z100100",
            "Sortie_id": "SortieB123",
            "uploading _time": "19062024Z091505",
        }
    )


@pytest.fixture
def message_processed():
    return {
        "image_id": "TEST_19062024_100010_0000",
        "Photo_time": "2024-06-19T10:01:00",
        "Sortie_id": "SortieB123",
        "uploading _time": "2024-06-19T09:15:05",
    }


@pytest.fixture
def times_message(date):
    return {
        "Photo_time": date,
        "uploading _time": date,
    }


@pytest.fixture
def current_path():
    return "services.information_entrance_approval"


@pytest.fixture
def class_path(current_path):
    return f"{current_path}.InformationEntranceApproval"


@pytest.fixture
def patch_process_dates(message_processed, current_path):
    return patch(
        f"{current_path}.process_dates",
        return_value=message_processed,
    )


def test_process_message(
    information_entrance_approval, message, message_processed, patch_process_dates
):
    with patch_process_dates as process_dates:
        new_message_processor = information_entrance_approval._process_message(message)
        assert new_message_processor == message_processed
        process_dates.assert_called_with(json.loads(message))


def test_post_process_message(
    information_entrance_approval,
    message_processed,
    patch_extracting_time_properties,
    patch_update_message,
    times_message,
    date,
):
    from utils.const import Indexes

    with patch_extracting_time_properties as extracting_time_properties, patch_update_message as _update_message:
        information_entrance_approval._post_process_message(message_processed)
        extracting_time_properties.assert_called_once_with(message_processed)
        _update_message.assert_called_once_with(
            times_message,
            Indexes.DATES,
            {"Photo_time": date},
        )
