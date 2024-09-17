from unittest.mock import Mock, call, patch

import pytest
from redis_cache.connect_redis import Redis


@pytest.fixture
def obj_name():
    return "test_obj"


@pytest.fixture
def folder_path():
    return "test_folder"


@pytest.fixture
def obj_properties():
    return "key", "value"


@pytest.fixture
def obj(obj_properties):
    key, value = obj_properties
    return {key: value}


@pytest.fixture
def json_objects():
    return [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]


@pytest.fixture
def existing_obj():
    return {"key1": "value1", "key2": "value2"}


@pytest.fixture
def expected_obj(obj, existing_obj):
    return {**existing_obj, **obj}


@pytest.fixture
def expected_folder_names():
    return ["folder1", "folder2", "folder3"]


@pytest.fixture
def expected_calls(folder_path):
    return [call(f"{folder_path}:1"), call(f"{folder_path}:2")]


@pytest.fixture
def expected_objects_calls(folder_path, json_objects):
    return [
        call(f"{folder_path}", "$", json_objects[0]),
        call(f"{folder_path}", "$", json_objects[1]),
    ]


@pytest.fixture
def expected_message_log():
    return "Successfully"


@pytest.fixture
def expected_message_log_error():
    return "Failed"


@pytest.fixture
def redis_instance():
    return Redis()


@pytest.fixture
def patch_Redis():
    return patch("redis_cache.connect_redis.redis.Redis")


@pytest.fixture
def patch_logger():
    return patch("redis_cache.connect_redis.logger", Mock())


@pytest.fixture
def mock_Redis(patch_Redis):
    with patch_Redis as mock_redis:
        yield mock_redis


@pytest.fixture
def mock_keys_redis(redis_instance, folder_path):
    return patch.object(
        redis_instance.connection,
        "keys",
        return_value=[f"{folder_path}:1", f"{folder_path}:2"],
    )


@pytest.fixture
def mock_set_redis(redis_instance):
    return patch.object(redis_instance.connection.json(), "set")


@pytest.fixture
def mock_get_redis(redis_instance, obj):
    return patch.object(redis_instance.connection.json(), "get", return_value=[obj])


@pytest.fixture
def mock_get_objects_redis(redis_instance, json_objects):
    return patch.object(
        redis_instance.connection.json(), "get", side_effect=json_objects
    )


@pytest.fixture
def mock_delete_redis(redis_instance):
    return patch.object(redis_instance.connection.json(), "delete")


@pytest.fixture
def mock_delete_objects_redis(redis_instance):
    return patch.object(redis_instance.connection, "delete")


@pytest.fixture
def mock_scan_redis(redis_instance, folder_path, expected_folder_names):
    return patch.object(
        redis_instance.connection,
        "scan",
        return_value=(
            0,
            [f"{folder_path}:{name}" for name in expected_folder_names],
        ),
    )


@pytest.fixture
def mock__get_json(redis_instance, obj):
    return patch.object(redis_instance, "_get_json", return_value=obj)


@pytest.fixture
def mock_add_obj_with_name_to_folder(redis_instance):
    return patch.object(redis_instance, "add_obj_to_folder")


@pytest.fixture
def mock_exists(redis_instance):
    return patch.object(redis_instance.connection, "exists", return_value=True)
