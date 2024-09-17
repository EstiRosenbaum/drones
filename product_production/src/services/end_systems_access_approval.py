import json

from data_processors.data_process_functions import process_dates, process_geo_shape
from listener_to_sender.listener_to_sender import ListenerToSender
from modules.calculate_area_per_sortie import get_area_for_sortie
from modules.sortie_functions import is_sortie_finished, sortie_already_exists
from pika import BlockingConnection
from redis_cache.connect_redis import Redis
from utils.const import FoldersInRedis, Indexes


class EndSystemsAccessApproval(ListenerToSender):
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

    def _process_message(self, message: str) -> object:
        message = json.loads(message)
        message["Footprint"] = process_geo_shape(message["Footprint"])
        message = process_dates(message)
        return message

    def _post_process_message(self, message: object) -> object:
        sortie_id = message["Sortie_id"]
        if not sortie_already_exists(self.redis, sortie_id):
            tagged_sortie = self._redis_actions(message, sortie_id)
            self._sortie_finished_process(sortie_id, tagged_sortie)

    def _redis_actions(self, message: object, sortie_id: str) -> object:
        self.redis.add_obj_to_folder(
            sortie_id, message["image_id"], message["Footprint"]
        )
        self._update_in_redis(sortie_id)
        tagged_sortie = self._get_from_redis(sortie_id)

        return tagged_sortie

    def _sortie_finished_process(self, sortie_id, tagged_sortie):
        is_finished = is_sortie_finished(
            self.redis, sortie_id, tagged_sortie["Number_of_images_tagged"]
        )
        if is_finished:
            self._save_tagged_sortie_in_sender(sortie_id, tagged_sortie)

    def _update_in_redis(self, sortie_id: str) -> None:
        self.redis.update_obj_by_name_and_folder(
            FoldersInRedis.COLLECTOR,
            sortie_id,
            counter_field_name_to_add="received_images",
        )

    def _get_from_redis(self, sortie_id: str) -> object:
        tagged_sortie = self.redis.get_obj_from_folder(
            sortie_id, FoldersInRedis.SORTIE
        )[0]

        return tagged_sortie

    def _save_tagged_sortie_in_sender(
        self, sortie_id: str, tagged_sortie: object
    ) -> None:
        tagged_sortie["Area"] = get_area_for_sortie(sortie_id, self.redis)
        self.save_message(tagged_sortie, Indexes.TAGGED_SORTIE)
