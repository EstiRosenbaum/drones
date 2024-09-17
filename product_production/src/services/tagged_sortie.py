import json

from data_processors.data_process_functions import process_dates
from listener_to_sender.listener_to_sender import ListenerToSender
from modules.calculate_area_per_sortie import get_area_for_sortie
from modules.sortie_functions import is_sortie_finished
from pika import BlockingConnection
from redis_cache.connect_redis import Redis
from utils.const import FoldersInRedis


class TaggedSortie(ListenerToSender):
    def __init__(
        self,
        queue_name: str,
        listener_type: str,
        connection: BlockingConnection,
        sender_type: str,
        redis: Redis,
    ) -> None:
        self.redis = redis
        super().__init__(queue_name, listener_type, connection, sender_type)

    def message_received_callback(self, message: str) -> None:
        message = json.loads(message)
        sortie_id = message.get("Sortie_id")
        is_finished = is_sortie_finished(
            self.redis, sortie_id, message["Number_of_images_tagged"]
        )

        if is_finished:
            message["Area"] = get_area_for_sortie(sortie_id, self.redis)
            self._save_message_in_sender(message)
        else:
            self._update_message_in_redis(message, sortie_id)

    def _save_message_in_sender(self, message: object) -> None:
        super().message_received_callback(message)

    def _update_message_in_redis(self, message: object, sortie_id: str) -> None:
        process_message = self._process_message(message)
        self._update_in_redis(sortie_id, process_message)

    def _update_in_redis(self, sortie_id, process_message):
        self.redis.update_obj_by_name_and_folder(
            sortie_id, FoldersInRedis.SORTIE, process_message
        )

    def _process_message(self, message: object) -> object:
        message = process_dates(message)
        return message
