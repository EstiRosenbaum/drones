from datetime import datetime, timedelta

from redis_cache.connect_redis import Redis
from utils.const import FoldersInRedis, Formats


def clearing_irrelevant_requests(redis: Redis) -> None:
    yesterday_date = _get_yesterday_date()
    redis.delete_folder(f"{FoldersInRedis.AREA_REQUESTS}:{yesterday_date}")
    redis.delete_folder(f"{FoldersInRedis.LOCATION_REQUESTS}:{yesterday_date}")


def _get_yesterday_date() -> datetime:
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime(Formats.DATE)
