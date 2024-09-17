from datetime import datetime

from helpers.logger.w_logger import logger

from data_processors.data_validation import is_valid_date, polygon_is_closed


def process_geo_point(geo_point: object) -> object:
    return {
        "coordinates": [geo_point["Longtitude"], geo_point["Latitude"]],
        "type": "Point",
    }


def process_geo_shape(footprint: list) -> object:
    if polygon_is_closed(footprint):
        return {"type": "Polygon", "coordinates": [footprint]}
    logger.error(
        "Error: first and last points of the poligon must be the same (it must close itself)."
    )
    return {"type": "Polygon", "coordinates": [[[]]]}


def process_geo_line(footprint: list) -> object:
    return {"type": "LineString", "coordinates": footprint}


def process_date(date: str) -> str:
    if is_valid_date(date):
        return f'{datetime.strptime(date, "%d%m%YZ%H%M%S").isoformat()}'
    logger.error(f"Error: the date {date} or date format in process is invalid.")
    return ""


def extracting_time_properties(obj: object) -> object:
    return {key: value for key, value in obj.items() if "time" in key}


def extracting_time_keys(obj: object) -> list:
    return [key for key in obj.keys() if "time" in key]


def process_dates(message: object) -> object:
    for key in extracting_time_keys(message):
        message[key] = process_date(message[key])
    return message
