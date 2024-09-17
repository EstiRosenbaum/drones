import json
from unittest.mock import Mock, patch

import pytest
from utils.const import FoldersInRedis


@pytest.fixture
def sortie_id():
    return "SortieB123"


@pytest.fixture
def message(sortie_id):
    return json.dumps(
        {
            "Sortie_id": sortie_id,
            "Photo_time": "22062024Z073021",
            "Landing_time": "22062024Z073021",
            "Start_Production_time": "22062024Z073021",
            "End_Production_time": "22062024Z073021",
            "Number_of_images_tagged": 3,
        },
    )


@pytest.fixture
def json_message(message):
    return json.loads(message)


@pytest.fixture
def message_processed():
    return {
        "Sortie_id": "sortie_id",
        "Photo_time": "2024-06-22T07:30:21",
        "Landing_time": "2024-06-22T07:30:21",
        "Start_Production_time": "2024-06-22T07:30:21",
        "End_Production_time": "2024-06-22T07:30:21",
        "Number_of_images_tagged": 3,
    }


@pytest.fixture
def sortie_finished_excepted():
    return [{"received_images": 3, "Number_of_images_tagged": 3}]


@pytest.fixture
def sortie_not_finished_excepted():
    return [{"received_images": 0, "Number_of_images_tagged": 2}]


@pytest.fixture
def redis_instance():
    return Mock()


@pytest.fixture
def current_path():
    return "services.tagged_sortie"


@pytest.fixture
def class_path(current_path):
    return f"{current_path}.TaggedSortie"


@pytest.fixture
def patch_sortie_finished(current_path):
    return patch(f"{current_path}.is_sortie_finished", return_value=True)


@pytest.fixture
def patch_sortie_not_finished(current_path):
    return patch(f"{current_path}.is_sortie_finished", return_value=False)


@pytest.fixture
def patch_save_message_in_sender(class_path):
    return patch(f"{class_path}._save_message_in_sender")


@pytest.fixture
def patch_update_message(class_path):
    return patch(f"{class_path}._update_message_in_redis")


@pytest.fixture
def patch_process_message(class_path, message_processed):
    return patch(
        f"{class_path}._process_message",
        return_value=message_processed,
    )


@pytest.fixture
def patch_process_dates(message_processed, current_path):
    return patch(f"{current_path}.process_dates", return_value=message_processed)


@pytest.fixture
def patch_listener_to_sender(current_path):
    return patch(f"{current_path}.ListenerToSender.message_received_callback")


def test_message_received_callback_save_message_in_sender(
    tagged_sortie,
    message,
    json_message,
    sortie_id,
    patch_sortie_finished,
    patch_save_message_in_sender,
    patch_calculate_area_per_sortie,
    redis_instance,
):
    with patch_calculate_area_per_sortie as calculate_area_per_sortie, patch_sortie_finished as sortie_finished, patch_save_message_in_sender as save_message:
        tagged_sortie.message_received_callback(message)
        calculate_area_per_sortie.assert_called_once_with(sortie_id, redis_instance)
        json_message["Area"] = calculate_area_per_sortie.return_value
        sortie_finished.assert_called_once_with(
            redis_instance, sortie_id, json_message["Number_of_images_tagged"]
        )
        save_message.assert_called_once_with(json_message)


def test_message_received_callback_update_message(
    tagged_sortie,
    message,
    sortie_id,
    patch_sortie_not_finished,
    patch_update_message,
    json_message,
    redis_instance,
):
    with patch_sortie_not_finished as sortie_finished, patch_update_message as update_message:
        tagged_sortie.message_received_callback(message)
        sortie_finished.assert_called_once_with(
            redis_instance, sortie_id, json_message["Number_of_images_tagged"]
        )
        update_message.assert_called_once_with(json_message, sortie_id)


def test_process_message(
    tagged_sortie, message_processed, patch_process_dates, json_message
):
    with patch_process_dates as process_dates:
        new_message_processor = tagged_sortie._process_message(json_message)
        assert new_message_processor == message_processed
        process_dates.assert_called_once_with(json_message)


def test_update_message_in_redis(
    tagged_sortie,
    sortie_id,
    patch_process_message,
    message_processed,
    json_message,
    redis_instance,
):
    redis_instance.update_obj_by_name_and_folder.return_value = Mock()
    with patch_process_message as process_message:
        tagged_sortie._update_message_in_redis(json_message, sortie_id)
        process_message.assert_called_once_with(json_message)
        tagged_sortie.redis.update_obj_by_name_and_folder.assert_called_once_with(
            sortie_id, FoldersInRedis.SORTIE, message_processed
        )


def test_save_message_in_sender(
    tagged_sortie,
    patch_listener_to_sender,
    json_message,
):
    with patch_listener_to_sender as listener:
        tagged_sortie._save_message_in_sender(json_message)
        listener.assert_called_once_with(json_message)
