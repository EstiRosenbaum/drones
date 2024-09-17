import datetime
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def expected_time_difference():
    return 90 * 60


@pytest.fixture
def date_with_datetime():
    return datetime.datetime(2024, 6, 22, 7, 52, 0, 0)


@pytest.fixture
def early_current_datetime():
    return datetime.datetime(2024, 6, 22, 5, 52, 0)


@pytest.fixture
def date_with_microsecond():
    return datetime.datetime(2024, 6, 22, 7, 52, 0, 10)


@pytest.fixture
def timestamp():
    return "2024-06-22T06:22:00"


@pytest.fixture
def date_with_strftime():
    return "2024-06-21"


@pytest.fixture
def sortie_id():
    return "SortieB123"


@pytest.fixture
def tagged_sortie():
    return "tagged_sortie"


@pytest.fixture
def time_and_counter_message(sortie_id):
    return [
        {
            sortie_id: {
                "Sortie_id": sortie_id,
                "timestamp": "2024-06-22T05:30:21",
                "tagged_images": "25",
                "image_counter": "12",
            },
            "SortieA123": {
                "Sortie_id": "SortieA123",
                "timestamp": "2024-06-22T07:36:21",
                "tagged_images": "32",
                "image_counter": "32",
            },
            "SortieA120": {
                "Sortie_id": "SortieA120",
                "timestamp": "2024-06-22T07:36:21",
                "tagged_images": "10",
                "image_counter": "10",
            },
        }
    ]


@pytest.fixture
def message(sortie_id):
    return {
        "Sortie_id": sortie_id,
        "Photo_time": "2024-06-22T07:30:21",
        "Landing_time": "2024-06-22T08:30:21",
        "Start_Production_time": "2024-06-22T09:30:21",
        "End_Production_time": "2024-06-22T09:52:21",
        "tagged": "25",
        "Area": "356.22",
    }


@pytest.fixture
def message_with_area(message):
    return {"sortie": message}


@pytest.fixture
def redis_cleaning_daily_path():
    return "process.redis_cleanup"


@pytest.fixture
def unfinished_sortie_process_path():
    return "process.calculate_unfinished_sortie"


@pytest.fixture
def get_time_difference_path(unfinished_sortie_process_path):
    return f"{unfinished_sortie_process_path}._get_time_difference"


@pytest.fixture
def get_current_time_path(unfinished_sortie_process_path):
    return f"{unfinished_sortie_process_path}._get_current_time"


@pytest.fixture
def is_time_difference_over_max_waiting_time_path(unfinished_sortie_process_path):
    return f"{unfinished_sortie_process_path}._is_time_difference_over_max_waiting_time"


@pytest.fixture
def patch_datetime(unfinished_sortie_process_path):
    return patch(f"{unfinished_sortie_process_path}.datetime")


@pytest.fixture
def patch_get_area_process(unfinished_sortie_process_path):
    return patch(
        f"{unfinished_sortie_process_path}.get_area_for_sortie",
        return_value=5,
    )


@pytest.fixture
def patch_get_yesterday_date(redis_cleaning_daily_path):
    return patch(f"{redis_cleaning_daily_path}._get_yesterday_date")


@pytest.fixture
def patch_date_time(redis_cleaning_daily_path):
    return patch(f"{redis_cleaning_daily_path}.datetime")


@pytest.fixture
def patch_small_time_difference(get_time_difference_path):
    return patch(
        get_time_difference_path,
        return_value=300,
    )


@pytest.fixture
def patch_time_difference(get_time_difference_path):
    return patch(
        get_time_difference_path,
        return_value=4000,
    )


@pytest.fixture
def patch_update_sortie_in_redis(unfinished_sortie_process_path):
    return patch(f"{unfinished_sortie_process_path}._update_sortie_in_redis")


@pytest.fixture
def patch_save_to_sender(unfinished_sortie_process_path):
    return patch(f"{unfinished_sortie_process_path}._save_in_sender")


@pytest.fixture
def patch_get_message_with_area(unfinished_sortie_process_path, message_with_area):
    return patch(
        f"{unfinished_sortie_process_path}._get_message",
        return_value=message_with_area,
    )


@pytest.fixture
def patch_current_time(get_current_time_path, date_with_datetime):
    return patch(
        get_current_time_path,
        return_value=date_with_datetime,
    )


@pytest.fixture
def patch_early_current_time(get_current_time_path, early_current_datetime):
    return patch(
        get_current_time_path,
        return_value=early_current_datetime,
    )


@pytest.fixture
def patch_is_time_difference_over_max_waiting_time(
    is_time_difference_over_max_waiting_time_path,
):
    return patch(is_time_difference_over_max_waiting_time_path, return_value=True)


@pytest.fixture
def patch_is_not_time_difference_over_max_waiting_time(
    is_time_difference_over_max_waiting_time_path,
):
    return patch(is_time_difference_over_max_waiting_time_path, return_value=False)


@pytest.fixture
def mock_redis():
    return Mock()


@pytest.fixture
def mock_listener_to_sender():
    return Mock()


@pytest.fixture
def mock_redis_time_and_counter(mock_redis, time_and_counter_message):
    mock_redis.get_folder_content.return_value = time_and_counter_message
    return mock_redis
