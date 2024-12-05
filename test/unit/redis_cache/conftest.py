from unittest.mock import patch

import pytest

from redis_cache.connect_redis import Redis

from .stub import (
    folder_path,
    value,
)


@pytest.fixture
def redis_instance():
    return Redis()


@pytest.fixture
def patch_Redis():
    return patch("redis_cache.connect_redis.redis.Redis")


@pytest.fixture
def mock_Redis(patch_Redis):
    with patch_Redis as mock_redis:
        yield mock_redis


@pytest.fixture
def mock_keys_redis(redis_instance):
    return patch.object(
        redis_instance.connection,
        "keys",
        return_value=[f"{folder_path}:1", f"{folder_path}:2"],
    )


@pytest.fixture
def mock_set_redis(redis_instance):
    return patch.object(redis_instance.connection, "set")


@pytest.fixture
def mock_get_redis(redis_instance):
    return patch.object(redis_instance.connection, "get", return_value=value)


@pytest.fixture
def mock_delete_redis(redis_instance):
    return patch.object(redis_instance.connection, "delete")


@pytest.fixture
def exception():
    return pytest.raises(Exception)
