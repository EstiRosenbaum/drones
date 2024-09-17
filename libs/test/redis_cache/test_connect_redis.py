import logging


def test_redis_connection(mock_Redis, redis_instance):
    assert mock_Redis.called
    mock_Redis.assert_called_with(host="redis", decode_responses=True)


def test_redis_connection_error(exception, mock_Redis, patch_logger):
    with exception, patch_logger as logger:
        assert mock_Redis.called
        mock_Redis.assert_called_with(host="redis", decode_responses=True)
        logger.error.assert_called()


def test_remove_obj_from_folder(
    caplog,
    expected_message_log,
    mock_Redis,
    folder_path,
    obj_name,
    mock_delete_redis,
    redis_instance,
):
    caplog.set_level(logging.INFO)
    with mock_delete_redis as mock_delete:
        redis_instance.remove_obj_from_folder(folder_path, obj_name)
        mock_delete.assert_called_once_with(f"{folder_path}:{obj_name}")
        assert expected_message_log in caplog.text


def test_failed_remove_obj_from_folder(
    exception,
    patch_logger,
    mock_Redis,
    redis_instance,
    folder_path,
    obj_name,
    mock_delete_redis,
    expected_message_log_error,
):
    with exception, mock_delete_redis as mock_delete, patch_logger as logger:
        redis_instance.remove_obj_from_folder(folder_path, obj_name)
        mock_delete.assert_called_once_with(f"{folder_path}:{obj_name}")
        logger.error.assert_called_once_with(expected_message_log_error)


def test_add_obj_to_folder(
    caplog,
    expected_message_log,
    mock_Redis,
    redis_instance,
    folder_path,
    obj,
    mock_set_redis,
    obj_name,
):
    caplog.set_level(logging.INFO)
    with mock_set_redis as mock_set:
        redis_instance.add_obj_to_folder(folder_path, obj_name, obj)
        mock_set.assert_called_once_with(f"{folder_path}:{obj_name}", "$", obj)
        assert expected_message_log in caplog.text


def test_failed_add_obj_to_folder(
    exception,
    patch_logger,
    mock_Redis,
    redis_instance,
    folder_path,
    obj,
    mock_set_redis,
    obj_name,
    expected_message_log_error,
):
    with exception, mock_set_redis as mock_set, patch_logger as logger:
        redis_instance.add_obj_to_folder(folder_path, obj_name, obj)
        mock_set.assert_called_once_with(f"{folder_path}:{obj_name}", "$", obj)
        logger.error.assert_called_once_with(expected_message_log_error)


def test_update_obj_by_name_and_folder(
    caplog,
    expected_message_log,
    mock_Redis,
    redis_instance,
    folder_path,
    obj_name,
    mock__get_json,
    mock_add_obj_with_name_to_folder,
):
    caplog.set_level(logging.INFO)
    with mock__get_json as _get_json, mock_add_obj_with_name_to_folder as add_obj_to_folder:
        redis_instance.update_obj_by_name_and_folder(folder_path, obj_name)
        _get_json.assert_called_once_with(f"{folder_path}:{obj_name}")
        add_obj_to_folder.assert_called_once()
        assert expected_message_log in caplog.text


def test_failed_update_obj_by_name_and_folder(
    exception,
    patch_logger,
    mock_Redis,
    redis_instance,
    folder_path,
    obj_name,
    mock__get_json,
    mock_add_obj_with_name_to_folder,
    expected_message_log_error,
):
    with exception, mock__get_json as _get_json, mock_add_obj_with_name_to_folder as add_obj_to_folder, patch_logger as logger:
        redis_instance.update_obj_by_name_and_folder(folder_path, obj_name)
        _get_json.assert_called_once_with(f"{folder_path}:{obj_name}")
        add_obj_to_folder.assert_called_once()
        logger.error.assert_called_once_with(expected_message_log_error)


def test__update_obj(mock_Redis, redis_instance, obj, existing_obj, expected_obj):
    result = redis_instance._update_obj(existing_obj, obj)
    assert result == expected_obj


def test_delete_folder(
    caplog,
    expected_message_log,
    mock_Redis,
    redis_instance,
    folder_path,
    mock_keys_redis,
    mock_delete_objects_redis,
    expected_calls,
):
    caplog.set_level(logging.INFO)
    with mock_keys_redis, mock_delete_objects_redis as mock_delete:
        redis_instance.delete_folder(folder_path)
        mock_delete.assert_has_calls(expected_calls)
        mock_delete.assert_called()
        assert expected_message_log in caplog.text


def test_failed_delete_folder(
    exception,
    patch_logger,
    mock_Redis,
    redis_instance,
    folder_path,
    mock_keys_redis,
    mock_delete_objects_redis,
    expected_calls,
    expected_message_log_error,
):
    with exception, mock_keys_redis, mock_delete_objects_redis as mock_delete, patch_logger as logger:
        redis_instance.delete_folder(folder_path)
        mock_delete.assert_has_calls(expected_calls)
        mock_delete.assert_called()
        logger.error.assert_called_once_with(expected_message_log_error)
    with mock_keys_redis:
        with mock_delete_objects_redis as mock_delete:
            redis_instance.delete_folder(folder_path)
            mock_delete.assert_has_calls(expected_calls)
            mock_delete.assert_called()


def test_get_field_from_obj_in_folder(
    caplog,
    mock_Redis,
    expected_message_log,
    redis_instance,
    obj_name,
    folder_path,
    obj_properties,
    mock__get_json,
):
    field_name, value = obj_properties
    caplog.set_level(logging.INFO)
    with mock__get_json:
        result = redis_instance.get_field_from_obj_in_folder(
            folder_path, obj_name, field_name
        )
        assert result == value
        assert expected_message_log in caplog.text


def test_field_get_field_from_obj_in_folder(
    exception,
    patch_logger,
    mock_Redis,
    redis_instance,
    obj_name,
    folder_path,
    obj_properties,
    mock__get_json,
    expected_message_log_error,
):
    field_name, value = obj_properties
    with exception, mock__get_json, patch_logger as logger:
        result = redis_instance.get_field_from_obj_in_folder(
            folder_path, obj_name, field_name
        )
        assert result == value
        logger.error.assert_called_once_with(expected_message_log_error)


def test_get_obj_from_folder(
    caplog,
    expected_message_log,
    mock_Redis,
    redis_instance,
    folder_path,
    obj_name,
    obj,
    mock_get_redis,
):
    caplog.set_level(logging.INFO)
    with mock_get_redis as mock_get:
        result = redis_instance.get_obj_from_folder(obj_name, folder_path)
        mock_get.assert_called_once_with(f"{obj_name}:{folder_path}", "$")
        assert result == obj
        assert expected_message_log in caplog.text


def test_field_get_obj_from_folder(
    exception,
    mock_Redis,
    redis_instance,
    patch_logger,
    folder_path,
    obj_name,
    obj,
    mock_get_redis,
    expected_message_log_error,
):
    with exception, mock_get_redis as mock_get, patch_logger as logger:
        result = redis_instance.get_obj_from_folder(obj_name, folder_path)
        mock_get.assert_called_once_with(f"{folder_path}:{obj_name}", "$")
        assert result == obj
        logger.error.assert_called_once_with(expected_message_log_error)


def test_get_folder_content(
    caplog,
    mock_Redis,
    expected_message_log,
    redis_instance,
    folder_path,
    json_objects,
    mock_keys_redis,
    mock_get_objects_redis,
):
    caplog.set_level(logging.INFO)
    with mock_keys_redis, mock_get_objects_redis:
        result = redis_instance.get_folder_content(folder_path)
        assert result == json_objects
        assert expected_message_log in caplog.text


def test_field_get_folder_content(
    exception,
    mock_Redis,
    patch_logger,
    expected_message_log_error,
    redis_instance,
    folder_path,
    json_objects,
    mock_keys_redis,
    mock_get_objects_redis,
):
    with exception, mock_keys_redis, mock_get_objects_redis, patch_logger as logger:
        result = redis_instance.get_folder_content(folder_path)
        assert result == json_objects
        logger.error.assert_called_once_with(expected_message_log_error)
    with mock_keys_redis:
        with mock_get_objects_redis:
            result = redis_instance.get_folder_content(folder_path)
            assert result == json_objects


def test_obj_exist(mock_Redis, redis_instance, mock_exists, folder_path, obj_name):
    with mock_exists as exists:
        result = redis_instance.obj_exist(folder_path, obj_name)
        exists.assert_called()
        assert result is True
