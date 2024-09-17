import json
from datetime import datetime

from data_processors.data_process_functions import process_dates
from listener_to_sender.listener_to_sender import ListenerToSender
from pika import BlockingConnection
from redis_cache.connect_redis import Redis
from utils.const import FoldersInRedis, Formats


class Sortie(ListenerToSender):
    def __init__(
        self,
        queue_name: str,
        listener_type: str,
        connection: BlockingConnection,
        sender_type: str,
        redis_connection: Redis,
    ) -> None:
        self.redis = redis_connection
        super().__init__(queue_name, listener_type, connection, sender_type)

    def message_received_callback(self, message: str) -> None:
        sortie_message, collector_message = self._process_message(message)
        sortie_id = sortie_message["Sortie_id"]
        self._save_in_redis(sortie_id, FoldersInRedis.SORTIE, sortie_message)
        self._save_in_redis(FoldersInRedis.COLLECTOR, sortie_id, collector_message)

    def _process_message(self, message: str) -> tuple[object, object]:
        sortie_message = self._sortie_message_process(message)
        collector_message = self._collector_message_process(sortie_message["Sortie_id"])
        return sortie_message, collector_message

    def _save_in_redis(self, folder: str, obj_name: str, message: object) -> None:
        self.redis.add_obj_to_folder(folder, obj_name, message)

    def _sortie_message_process(self, message: str) -> object:
        sortie_message = process_dates(json.loads(message))
        return sortie_message

    def _collector_message_process(
        self,
        sortie_id: str,
    ) -> object:
        return {
            "timestamp": datetime.now().strftime(Formats.DATE),
            "received_images": 0,
            "Sortie_id": sortie_id,
        }
