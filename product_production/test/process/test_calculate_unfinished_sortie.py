from datetime import datetime

from process.calculate_unfinished_sortie import (
    _get_current_time,
    _get_message,
    _get_time_difference,
    _is_time_difference_over_max_waiting_time,
    _save_in_sender,
    _update_sortie_in_redis,
    calculate_unfinished_sortie,
)
from utils.const import FoldersInRedis, Formats, Indexes


def test_calculate_unfinished_sortie_with_message_before_time(
    mock_redis_time_and_counter,
    mock_listener_to_sender,
    patch_save_to_sender,
    patch_get_message_with_area,
    patch_is_not_time_difference_over_max_waiting_time,
    patch_update_sortie_in_redis,
):
    with patch_save_to_sender as _save_to_sender, patch_get_message_with_area as _get_message, patch_is_not_time_difference_over_max_waiting_time as difference_over_max_waiting_time, patch_update_sortie_in_redis as _update_sortie:
        calculate_unfinished_sortie(
            mock_redis_time_and_counter, mock_listener_to_sender
        )
        difference_over_max_waiting_time.assert_called()
        _save_to_sender.assert_not_called()
        _get_message.assert_not_called()
        _update_sortie.assert_not_called()


def test_process_with_all_messages_after_time(
    mock_redis_time_and_counter,
    mock_listener_to_sender,
    patch_save_to_sender,
    patch_get_message_with_area,
    patch_update_sortie_in_redis,
    patch_is_time_difference_over_max_waiting_time,
):
    patch_get_message_with_area = patch_get_message_with_area.start()
    with patch_save_to_sender as _save_in_sender, patch_get_message_with_area, patch_update_sortie_in_redis as _update_sortie, patch_is_time_difference_over_max_waiting_time:
        calculate_unfinished_sortie(
            mock_redis_time_and_counter, mock_listener_to_sender
        )
        patch_is_time_difference_over_max_waiting_time.call_count = 3
        patch_get_message_with_area.call_count = 3
        _save_in_sender.call_count = 3
        _update_sortie.call_count = 3


def test_process_with_message_after_time(
    patch_save_to_sender,
    patch_current_time,
    mock_redis_time_and_counter,
    mock_listener_to_sender,
    patch_get_message_with_area,
    patch_update_sortie_in_redis,
    message_with_area,
    sortie_id,
):
    patch_get_message_with_area = patch_get_message_with_area.start()
    with patch_current_time, patch_save_to_sender as mock_save_in_sender, patch_get_message_with_area, patch_update_sortie_in_redis as _update_sortie:
        calculate_unfinished_sortie(
            mock_redis_time_and_counter, mock_listener_to_sender
        )
        patch_get_message_with_area.assert_called_once_with(
            mock_redis_time_and_counter, sortie_id
        )
        mock_save_in_sender.assert_called_once_with(
            message_with_area, mock_listener_to_sender
        )
        _update_sortie.assert_called_once_with(
            mock_redis_time_and_counter, message_with_area
        )


def test_is_time_difference_over_max_waiting_time(patch_time_difference, timestamp):
    with patch_time_difference as time_difference:
        is_max = _is_time_difference_over_max_waiting_time(timestamp)
        time_difference.assert_called_once_with(timestamp)
        assert is_max is True


def test_is_time_difference_less_then_max_waiting_time(
    patch_small_time_difference, timestamp
):
    with patch_small_time_difference as time_difference:
        is_max = _is_time_difference_over_max_waiting_time(timestamp)
        time_difference.assert_called_once_with(timestamp)
        assert is_max is False


def test_get_message(patch_get_area_process, mock_redis_time_and_counter, sortie_id):
    with patch_get_area_process as get_area_process:
        result = _get_message(mock_redis_time_and_counter, sortie_id)
        mock_redis_time_and_counter.get_folder_content.assert_called_with(sortie_id)
        get_area_process.assert_called_with(sortie_id, mock_redis_time_and_counter)
        assert result["Area"] == get_area_process.return_value


def test_save_in_sender(mock_listener_to_sender, message_with_area):
    _save_in_sender(
        message=message_with_area, listener_to_sender_instance=mock_listener_to_sender
    )

    mock_listener_to_sender._save_in_sender.assert_called_once_with(
        message_with_area, Indexes.TAGGED_SORTIE
    )


def test_update_uploaded_sortie_in_redis(
    mock_redis_time_and_counter, message, sortie_id
):
    _update_sortie_in_redis(mock_redis_time_and_counter, message)
    mock_redis_time_and_counter.add_obj_to_folder.assert_called_with(
        FoldersInRedis.SORTIES_UPLOADED,
        sortie_id,
        {"timestamp": datetime.now().strftime(Formats.DATE), "Sortie_id": sortie_id},
    )


def test_get_time_difference(patch_current_time, timestamp, expected_time_difference):
    with patch_current_time:
        actual_time_difference = _get_time_difference(timestamp)
        assert actual_time_difference == expected_time_difference


def test_get_current_time(patch_datetime, date_with_microsecond, date_with_datetime):
    with patch_datetime as _datetime:
        _datetime.now.return_value = date_with_microsecond
        result = _get_current_time()
        assert result == date_with_datetime
