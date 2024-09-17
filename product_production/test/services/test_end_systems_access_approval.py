import json
from unittest.mock import Mock, patch

import pytest
from utils.const import FoldersInRedis, Indexes


@pytest.fixture
def sortie_id():
    return "SortieB123"


@pytest.fixture
def footprint():
    return {
        "type": "Polygon",
        "coordinates": [
            [
                [32.113225, 34.786673],
                [32.10, 34.70],
                [32.11, 34.71],
                [32.113225, 34.786673],
            ]
        ],
    }


@pytest.fixture
def basic_message(sortie_id):
    return {
        "image_id": "TEST_19062024_100010_0000",
        "Sortie_id": sortie_id,
        "Algorithmic_registraion": True,
        "Prev_image_id": "TEST_19062024_100005_0000",
        "Next_image_id": "TEST_19062024_100010_0001",
        "Prev_image_tie_points": "url",
        "Next_image_tie_points": "url",
    }


@pytest.fixture
def message(basic_message):
    return json.dumps(
        {
            **basic_message,
            "Photo_time": "19062024Z100100",
            "Creation_time": "19062024Z100100",
            "Footprint": [
                [32.113225, 34.786673],
                [32.10, 34.70],
                [32.11, 34.71],
                [32.113225, 34.786673],
            ],
        }
    )


@pytest.fixture
def json_message(message):
    return json.loads(message)


@pytest.fixture
def in_message_processed(basic_message, footprint):
    return {
        **basic_message,
        "Photo_time": "19062024Z100100",
        "Creation_time": "19062024Z100100",
        "Footprint": footprint,
    }


@pytest.fixture
def message_processed(basic_message, footprint):
    return {
        **basic_message,
        "Photo_time": "2024-06-19T10:01:00",
        "Creation_time": "2024-06-19T10:01:00",
        "Footprint": footprint,
    }


@pytest.fixture
def tagged_sortie_message(sortie_id):
    return {
        "Sortie_id": sortie_id,
        "Photo_time": "2024-06-22T07:30:21",
        "Platform_name": "PlatformA",
        "Sensor_type": "SensorA",
        "Platform_id": "PlatformA123",
        "Landing_time": "2024-06-22T07:30:21",
        "Start_Production_time": "2024-06-22T07:30:21",
        "End_Production_time": "2024-06-22T07:30:21",
        "Sensor_id": "SensorA123",
        "Number_of_images": 1000,
        "Number_of_images_tagged": 3,
    }


@pytest.fixture
def image_id(message_processed):
    return message_processed["image_id"]


@pytest.fixture
def number_of_images_tagged(tagged_sortie_message):
    return tagged_sortie_message["Number_of_images_tagged"]


@pytest.fixture
def current_path():
    return "services.end_systems_access_approval"


@pytest.fixture
def class_path(current_path):
    return f"{current_path}.EndSystemsAccessApproval"


@pytest.fixture
def patch_process_dates(message_processed, current_path):
    return patch(f"{current_path}.process_dates", return_value=message_processed)


@pytest.fixture
def patch_process_geo_shape(message_processed, current_path):
    return patch(
        f"{current_path}.process_geo_shape", return_value=message_processed["Footprint"]
    )


@pytest.fixture
def patch_unfinished_sortie(current_path):
    return patch(f"{current_path}.is_sortie_finished", return_value=False)


@pytest.fixture
def patch_finished_sortie(current_path):
    return patch(f"{current_path}.is_sortie_finished", return_value=True)


@pytest.fixture
def patch_redis_actions(class_path, tagged_sortie_message):
    return patch(f"{class_path}._redis_actions", return_value=tagged_sortie_message)


@pytest.fixture
def patch_update_in_redis(class_path):
    return patch(f"{class_path}._update_in_redis")


@pytest.fixture
def patch_sortie_finished_process(class_path):
    return patch(f"{class_path}._sortie_finished_process")


@pytest.fixture
def patch_get_from_redis(class_path, tagged_sortie_message):
    return patch(f"{class_path}._get_from_redis", return_value=tagged_sortie_message)


@pytest.fixture
def patch_save_tagged_sortie_in_sender(class_path):
    return patch(f"{class_path}._save_tagged_sortie_in_sender")


@pytest.fixture
def patch_sortie_already_exists(current_path):
    return patch(f"{current_path}.sortie_already_exists", return_value=True)


@pytest.fixture
def patch_sortie_not_already_exists(current_path):
    return patch(f"{current_path}.sortie_already_exists", return_value=False)


def test_process_message(
    end_systems_access_approval,
    message,
    json_message,
    message_processed,
    in_message_processed,
    patch_process_dates,
    patch_process_geo_shape,
):
    with patch_process_dates as process_dates, patch_process_geo_shape as process_geo_shape:
        new_message_processor = end_systems_access_approval._process_message(message)
        process_geo_shape.assert_called_once_with(json_message["Footprint"])
        process_dates.assert_called_once_with(in_message_processed)
        assert new_message_processor == message_processed


def test_post_process_message_with_sortie_not_exists(
    end_systems_access_approval,
    message_processed,
    sortie_id,
    patch_sortie_finished_process,
    patch_redis_actions,
    patch_sortie_not_already_exists,
    tagged_sortie_message,
):
    with patch_sortie_not_already_exists, patch_redis_actions as redis_actions, patch_sortie_finished_process as sortie_finished_process:
        end_systems_access_approval._post_process_message(message_processed)
        redis_actions.assert_called_once_with(message_processed, sortie_id)
        sortie_finished_process.assert_called_once_with(
            sortie_id, tagged_sortie_message
        )


def test_post_process_message_with_sortie_exists(
    end_systems_access_approval,
    message_processed,
    patch_sortie_already_exists,
    patch_sortie_finished_process,
    patch_redis_actions,
):
    with patch_sortie_already_exists, patch_redis_actions as redis_actions, patch_sortie_finished_process as sortie_finished_process:
        end_systems_access_approval._post_process_message(message_processed)
        redis_actions.assert_not_called()
        sortie_finished_process.assert_not_called()


def test_redis_action(
    end_systems_access_approval,
    message_processed,
    sortie_id,
    image_id,
    footprint,
    patch_get_from_redis,
    patch_update_in_redis,
    mock_redis,
):
    with patch_update_in_redis as update_in_redis, patch_get_from_redis as get_in_redis:
        end_systems_access_approval._redis_actions(message_processed, sortie_id)
        mock_redis.add_obj_to_folder.return_value = Mock()
        end_systems_access_approval.redis.add_obj_to_folder.assert_called_once_with(
            sortie_id, image_id, footprint
        )
        update_in_redis.assert_called_once_with(sortie_id)
        get_in_redis.assert_called_once_with(sortie_id)


def test_sortie_finished_process(
    end_systems_access_approval,
    patch_finished_sortie,
    patch_save_tagged_sortie_in_sender,
    sortie_id,
    tagged_sortie_message,
    mock_redis,
):
    with patch_finished_sortie as finished_sortie, patch_save_tagged_sortie_in_sender as save_in_sender:
        end_systems_access_approval._sortie_finished_process(
            sortie_id, tagged_sortie_message
        )
        finished_sortie.assert_called_with(
            mock_redis, sortie_id, tagged_sortie_message["Number_of_images_tagged"]
        )
        assert finished_sortie.return_value is True
        save_in_sender.assert_called_with(sortie_id, tagged_sortie_message)


def test_sortie_unfinished_process(
    end_systems_access_approval,
    patch_unfinished_sortie,
    patch_save_tagged_sortie_in_sender,
    sortie_id,
    tagged_sortie_message,
    mock_redis,
):
    with patch_unfinished_sortie as unfinished_sortie, patch_save_tagged_sortie_in_sender as save_in_sender:
        end_systems_access_approval._sortie_finished_process(
            sortie_id, tagged_sortie_message
        )
        unfinished_sortie.assert_called_with(
            mock_redis, sortie_id, tagged_sortie_message["Number_of_images_tagged"]
        )
        assert unfinished_sortie.return_value is False
        save_in_sender.assert_not_called()


def test_update_in_redis(end_systems_access_approval, sortie_id, mock_redis):
    mock_redis.update_obj_by_name_and_folder.return_value = Mock()
    end_systems_access_approval._update_in_redis(sortie_id)
    end_systems_access_approval.redis.update_obj_by_name_and_folder.assert_called_once_with(
        FoldersInRedis.COLLECTOR, sortie_id, counter_field_name_to_add="received_images"
    )


def test_get_from_redis(
    end_systems_access_approval, sortie_id, tagged_sortie_message, mock_redis
):
    mock_redis.get_obj_from_folder.return_value = [tagged_sortie_message]
    end_systems_access_approval._get_from_redis(sortie_id)
    end_systems_access_approval.redis.get_obj_from_folder.assert_called_once_with(
        sortie_id, FoldersInRedis.SORTIE
    )


def test_save_tagged_sortie_in_sender(
    end_systems_access_approval,
    tagged_sortie_message,
    sortie_id,
    patch_save_message,
    patch_calculate_area_per_sortie,
    mock_redis,
):
    with patch_save_message as save_message, patch_calculate_area_per_sortie as calculate_area_per_sortie:
        end_systems_access_approval._save_tagged_sortie_in_sender(
            sortie_id, tagged_sortie_message
        )
        calculate_area_per_sortie.assert_called_once_with(sortie_id, mock_redis)
        tagged_sortie_message["Area"] = calculate_area_per_sortie.return_value
        save_message.assert_called_once_with(
            tagged_sortie_message, Indexes.TAGGED_SORTIE
        )
