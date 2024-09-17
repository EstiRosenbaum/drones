from redis_cache.connect_redis import Redis
from utils.const import FoldersInRedis


def is_sortie_finished(redis: Redis, sortie_id: str, tagged_images: int) -> bool:
    counter = redis.get_obj_from_folder(FoldersInRedis.COLLECTOR, sortie_id)[0]
    return tagged_images == counter.get("received_images")


def sortie_already_exists(redis: Redis, sortie_id: str) -> bool:
    return redis.obj_exist(FoldersInRedis.SORTIES_UPLOADED, sortie_id)
