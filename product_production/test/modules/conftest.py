from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def short_message():
    return 10.2


@pytest.fixture
def number_of_images_tagged():
    return 3


@pytest.fixture
def sortie_finished_excepted():
    return [{"received_images": 3, "Number_of_images_tagged": 3}]


@pytest.fixture
def sortie_not_finished_excepted():
    return [{"received_images": 0, "Number_of_images_tagged": 2}]


@pytest.fixture
def error_message():
    return "failed to delete folder"


@pytest.fixture
def error_message_save_area_in_elastic():
    return "failed to save unfinished sortie after calculating area"


@pytest.fixture
def coordinates_obj():
    return {"coordinates": [[[10.2, 20.2], [15.2, 21.3], [15.8, 22.0], [10.2, 20.2]]]}


@pytest.fixture
def coordinates():
    return [
        [[11.2, 20.2], [15.2, 21.3], [15.8, 22.0], [11.2, 20.2]],
        [[12.2, 20.2], [13.2, 21.3], [15.8, 22.0], [12.2, 20.2]],
        [[14.2, 20.2], [15.2, 21.3], [15.8, 22.0], [14.2, 20.2]],
    ]


@pytest.fixture
def sortie_id():
    return "SortieB123"


@pytest.fixture
def messages(sortie_id):
    return [
        {
            "sortie": {
                "Sortie_id": sortie_id,
                "Photo_time": "2024-06-22T07:30:21",
                "Landing_time": "2024-06-22T08:30:21",
                "Start_Production_time": "2024-06-22T09:30:21",
                "End_Production_time": "2024-06-22T09:52:21",
                "tagged": "25",
            },
            "img_1000": {
                "coordinates": [
                    [[11.2, 20.2], [15.2, 21.3], [15.8, 22.0], [11.2, 20.2]]
                ]
            },
            "img_1001": {
                "coordinates": [
                    [[12.2, 20.2], [13.2, 21.3], [15.8, 22.0], [12.2, 20.2]]
                ]
            },
            "img_1002": {
                "coordinates": [
                    [[14.2, 20.2], [15.2, 21.3], [15.8, 22.0], [14.2, 20.2]]
                ]
            },
        }
    ]


@pytest.fixture
def obj_without_coordinates(sortie_id):
    return {"image_name": "img_123", "sortie": sortie_id}


@pytest.fixture
def exception_with_error_instance(error_message):
    return Exception(error_message)


@pytest.fixture
def patch_getArea(mock_get_area):
    return patch(
        "modules.calculate_area_per_sortie.get_area_in_km",
        return_value=mock_get_area,
    )


@pytest.fixture
def current_path():
    return "modules.calculate_area_per_sortie"


@pytest.fixture
def patch_logger(current_path):
    return patch(f"{current_path}.logger", Mock())


@pytest.fixture
def patch_mock_tagged_sortie(unfinished_sortie_process_path):
    return patch(f"{unfinished_sortie_process_path}.tagged_sortie", return_value=Mock())


@pytest.fixture
def patch_datetime(unfinished_sortie_process_path):
    return patch(f"{unfinished_sortie_process_path}.datetime")


@pytest.fixture
def mock_listener_to_sender():
    listener_to_sender = Mock()
    return listener_to_sender


@pytest.fixture
def mock_tagged_sortie():
    tagged_sortie = Mock()
    return tagged_sortie


@pytest.fixture
def mock_get_area():
    get_area_in_km = Mock()
    get_area_in_km.return_value = 1234.05
    return get_area_in_km.return_value


@pytest.fixture
def mock_redis_sorties(messages):
    mock_redis = Mock()
    mock_redis.get_folder_content.return_value = messages
    return mock_redis
