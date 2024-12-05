from .stub import folder_path, obj_name, value


def test_redis_connection(mock_Redis, redis_instance):
    assert mock_Redis.called
    mock_Redis.assert_called_with(host="redis", decode_responses=True)


def test_redis_connection_error(exception, mock_Redis):
    with exception:
        assert mock_Redis.called
        mock_Redis.assert_called_with(host="redis", decode_responses=True)


def test_update_value_to_folder(
    mock_Redis,
    redis_instance,
    mock_set_redis,
):
    with mock_set_redis as mock_set:
        redis_instance.update_value_to_folder(folder_path, obj_name, value)
        mock_set.assert_called_once_with(f"{folder_path}:{obj_name}", value)


def test_remove_value_from_folder(
    mock_Redis,
    redis_instance,
    mock_delete_redis,
):
    with mock_delete_redis as mock_delete:
        redis_instance.remove_value_from_folder(folder_path, obj_name)
        mock_delete.assert_called_once_with(f"{folder_path}:{obj_name}")


def test_get_keys(
    mock_Redis,
    redis_instance,
    mock_keys_redis,
):
    with mock_keys_redis as mock_keys:
        redis_instance.get_keys(folder_path)
        mock_keys.assert_called_once_with(f"{folder_path}:*")


def test_get_value(
    mock_Redis,
    redis_instance,
    mock_get_redis,
):
    with mock_get_redis as mock_value:
        redis_instance.get_value(folder_path)
        mock_value.assert_called_once_with(folder_path)
