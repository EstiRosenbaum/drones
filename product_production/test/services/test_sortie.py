import json
from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from utils.const import FoldersInRedis, Formats


@pytest.fixture
def sortie_id():
    return "SortieB123"


@pytest.fixture
def message():
    return json.dumps(
        {
            "Sortie_id": "SortieB123",
            "Photo_time": "22062024Z073021",
            "Platform_name": "PlatformA",
            "Sensor_type": "SensorA",
            "Platform_id": "PlatformA123",
            "Sensor_id": "SensorA123",
            "Landing_time": "22062024Z073021",
            "Number_of_images": "1000",
        },
    )


@pytest.fixture
def message_processed():
    return {
        "Sortie_id": "SortieB123",
        "Photo_time": "2024-06-22T07:30:21",
        "Platform_name": "PlatformA",
        "Sensor_type": "SensorA",
        "Platform_id": "PlatformA123",
        "Sensor_id": "SensorA123",
        "Landing_time": "2024-06-22T07:30:21",
        "Number_of_images": "1000",
    }


@pytest.fixture
def collector_message_processed(sortie_id):
    return {
        "timestamp": datetime.now().strftime(Formats.DATE),
        "received_images": 0,
        "Sortie_id": sortie_id,
    }


@pytest.fixture
def current_path():
    return "services.sortie"


@pytest.fixture
def class_path(current_path):
    return f"{current_path}.Sortie"


@pytest.fixture
def patch_sortie_message_process(class_path, sortie_id):
    return patch(
        f"{class_path}._sortie_message_process",
        return_value={"Sortie_id": sortie_id},
    )


@pytest.fixture
def patch_time_and_counter_collector_message_process(
    class_path, collector_message_processed
):
    return patch(
        f"{class_path}._collector_message_process",
        return_value=collector_message_processed,
    )


@pytest.fixture
def patch_save_in_redis(class_path):
    return patch(
        f"{class_path}._save_in_redis",
        return_value=Mock(),
    )


@pytest.fixture
def patch_process_message(class_path, message_processed, collector_message_processed):
    messages = message_processed, collector_message_processed
    return patch(
        f"{class_path}._process_message",
        return_value=messages,
    )


def test_message_received_callback(
    sortie, message, patch_process_message, patch_save_in_redis
):
    with patch_save_in_redis as redis, patch_process_message as process:
        sortie.message_received_callback(message)
        process.assert_called_once_with(message)
        redis.assert_called()
        assert redis.call_count == 2


def test_process_message(
    sortie,
    message,
    patch_sortie_message_process,
    patch_time_and_counter_collector_message_process,
    sortie_id,
):
    with patch_sortie_message_process as sortie_message, patch_time_and_counter_collector_message_process as collector_message:
        sortie._process_message(message)
        sortie_message.assert_called_once_with(message)
        collector_message.assert_called_once_with(sortie_id)


def test_sortie_message_process(sortie, message, message_processed):
    new_message_processor = sortie._sortie_message_process(message)
    assert new_message_processor == message_processed


def test_collector_message_process(sortie, collector_message_processed, sortie_id):
    new_message_processor = sortie._collector_message_process(sortie_id)
    assert new_message_processor == collector_message_processed


def test_save_in_redis(sortie, sortie_id, message_processed):
    sortie._save_in_redis(sortie_id, FoldersInRedis.SORTIE, message_processed)
    sortie.redis.add_obj_to_folder.assert_called_once_with(
        sortie_id, FoldersInRedis.SORTIE, message_processed
    )
