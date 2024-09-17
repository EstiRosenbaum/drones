from datetime import datetime

from helpers.logger.w_logger import logger
from listener_to_sender.listener_to_sender import ListenerToSender
from modules.calculate_area_per_sortie import get_area_for_sortie
from redis_cache.connect_redis import Redis
from utils.const import FoldersInRedis, Formats, Indexes, ProcessEnvs


def calculate_unfinished_sortie(
    redis: Redis, listener_to_sender_instance: ListenerToSender
) -> None:
    all_sorties = redis.get_folder_content(FoldersInRedis.COLLECTOR)[0]
    for sortie_id in all_sorties.keys():
        time = all_sorties[sortie_id].get("timestamp")
        if _is_time_difference_over_max_waiting_time(time):
            message = _get_message(redis, sortie_id)
            _save_in_sender(message, listener_to_sender_instance)
            _update_sortie_in_redis(redis, message)


def _is_time_difference_over_max_waiting_time(time: str) -> bool:
    return _get_time_difference(time) > ProcessEnvs.MAX_WAITING_TIME


def _get_message(redis: Redis, sortie_id: str) -> object:
    message = redis.get_folder_content(sortie_id)[0]
    message["Area"] = get_area_for_sortie(sortie_id, redis)
    return message


def _save_in_sender(
    message: object, listener_to_sender_instance: ListenerToSender
) -> None:
    try:
        listener_to_sender_instance._save_in_sender(message, Indexes.TAGGED_SORTIE)
    except Exception as error:
        logger.error(f"Failed to save the message in sender - {error}.")


def _update_sortie_in_redis(redis: Redis, message: object):
    sortie_id = message["Sortie_id"]
    redis.add_obj_to_folder(
        FoldersInRedis.SORTIES_UPLOADED,
        sortie_id,
        {"timestamp": datetime.now().strftime(Formats.DATE), "Sortie_id": sortie_id},
    )


def _get_time_difference(time: str) -> int:
    return (
        _get_current_time() - datetime.strptime(time, Formats.DATE_TIME)
    ).total_seconds()


def _get_current_time() -> datetime:
    return datetime.now().replace(microsecond=0)
