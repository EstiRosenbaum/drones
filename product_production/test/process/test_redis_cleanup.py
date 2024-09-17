from process.redis_cleanup import _get_yesterday_date, clearing_irrelevant_requests


def test_clearing_irrelevant_requests(patch_get_yesterday_date, mock_redis):
    with patch_get_yesterday_date as get_yesterday_date:
        clearing_irrelevant_requests(mock_redis)
        get_yesterday_date.assert_called()
        mock_redis.delete_folder.assert_called()
        assert mock_redis.delete_folder.call_count == 2


def test_get_yesterday_date(patch_date_time, date_with_datetime, date_with_strftime):
    with patch_date_time as date_time:
        date_time.now.return_value = date_with_datetime
        date_time.strftime.return_value = date_with_strftime
        result = _get_yesterday_date()
        assert result == date_with_strftime
