from data_processors.data_validation import (
    date_format,
    date_length,
    is_valid_date,
    polygon_is_closed,
)


def test_date_format():
    correct_date = "12121200Z414141"
    short_date = "1212120Z414141"
    misformed_date = "1212Z1201414141"
    assert date_format(correct_date) is True
    assert date_format(short_date) is False
    assert date_format(misformed_date) is False


def test_date_length():
    date = "12121120Z414141"
    short_date = "1211120Z414141"
    long_date = "121211110Z414141"
    assert date_length(date) is True
    assert date_length(short_date) is False
    assert date_length(long_date) is False


def test_polygon():
    closed_polygon = [[1.2, 1.3], [2.3, 2.3], [4.5, 4.4], [1.2, 1.3]]
    open_polygon = [[1.2, 1.3], [2.3, 2.3], [4.5, 4.4], [1.33, 3.2]]
    assert polygon_is_closed(closed_polygon) is True
    assert polygon_is_closed(open_polygon) is False


def test_is_valid_date():
    date = "12336512Z455615"
    short_date = "123365Z4556"
    assert is_valid_date(date) is True
    assert is_valid_date(short_date) is False
