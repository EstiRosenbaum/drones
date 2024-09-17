import logging

from data_processors.data_process_functions import (
    extracting_time_keys,
    extracting_time_properties,
    process_date,
    process_dates,
    process_geo_line,
    process_geo_point,
    process_geo_shape,
)


def test_convert_to_geo_point(point, expected_geo_point):
    assert process_geo_point(point) == expected_geo_point


def test_convert_to_geo_shape(footprint_to_geo_shape, expected_geo_shape):
    assert process_geo_shape(footprint_to_geo_shape) == expected_geo_shape


def test_convert_to_geo_line(footprint_to_geo_line, expected_geo_line):
    assert process_geo_line(footprint_to_geo_line) == expected_geo_line


def test_convert_date(date, expected_date):
    assert process_date(date) == expected_date


def test_extracting_time_properties(message, times_message):
    assert extracting_time_properties(message) == times_message


def test_extracting_time_keys(message, times_keys):
    assert extracting_time_keys(message) == times_keys


def test_failed_convert_to_geo_shape(
    caplog, failed_footprint, expected_failed_geo_shape, expected_message_log
):
    caplog.set_level(logging.ERROR)
    assert process_geo_shape(failed_footprint) == expected_failed_geo_shape
    assert expected_message_log in caplog.text


def test_process_dates(
    message,
    message_processed,
    patch_extracting_time_keys,
    patch_process_date,
):
    with patch_extracting_time_keys as extracting_time_keys, patch_process_date as process_date:
        message_with_process_dates = process_dates(message)
        assert message_with_process_dates == message_processed
        extracting_time_keys.assert_called_once_with(message)
        process_date.assert_called()
        assert process_date.call_count == 2


def test_process_dates_invalid(
    caplog, exception, invalid_date, expected_error_message_log
):
    caplog.set_level(logging.ERROR)
    with exception:
        assert process_date(invalid_date) == ""
        assert expected_error_message_log in caplog.text
