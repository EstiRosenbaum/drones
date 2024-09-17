from typing import Any

from helpers.logger.w_logger import logger
from redis_cache.connect_redis import Redis
from utils.const import FoldersInRedis

from .calculate_area import get_area_in_km


def get_area_for_sortie(sortie_id: str, redis_connection: Redis) -> Any:
    footprints = _get_footprints_from_redis(sortie_id, redis_connection)
    try:
        area = get_area_in_km(footprints)
        _remove_from_redis(sortie_id, redis_connection)
        return area
    except Exception as error:
        logger.error(f"Failed to get area for {sortie_id} - {error}")


def _get_footprints_from_redis(sortie_id: str, redis_connection: Redis) -> list:
    doc = redis_connection.get_folder_content(sortie_id)[0]
    footprints = _get_footprints_from_doc(doc)
    return footprints


def _get_footprints_from_doc(doc: list) -> list:
    return [
        message.get("coordinates")[0]
        for key, message in doc.items()
        if _contains_coordinates(message)
    ]


def _contains_coordinates(message: Any) -> bool:
    return isinstance(message, dict) and "coordinates" in message


def _remove_from_redis(sortie_id: str, redis_connection: Redis) -> None:
    redis_connection.delete_folder(sortie_id)
    redis_connection.remove_obj_from_folder(FoldersInRedis.COLLECTOR, sortie_id)
