import re


def polygon_is_closed(polygon: list) -> bool:
    return polygon[0] == polygon[-1]


def date_length(date: str) -> bool:
    return len(date) == 15


def date_format(date: str) -> bool:
    return re.match(r"^\d{8}Z\d{6}$", date) is not None


def is_valid_date(date: str) -> bool:
    return date_length(date) and date_format(date)
