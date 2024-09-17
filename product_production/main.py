import os

import schedule
from dotenv import load_dotenv
from helpers.utils.const import Listener, Sender
from listener.rabbitmq.connection import Connection
from listener_to_sender.listener_to_sender import ListenerToSender
from modules.classes_activating_process import classes_activating_process
from process.calculate_unfinished_sortie import calculate_unfinished_sortie
from redis_cache.connect_redis import Redis
from utils.const import Indexes, ProcessEnvs

load_dotenv()


def main() -> None:
    connection = Connection()
    redis = Redis()
    class_files = os.listdir("product_production/src/services")
    classes_activating_process(class_files, connection, redis)

    listener_to_sender = ListenerToSender(
        Indexes.TAGGED_SORTIE,
        Listener.RABBITMQ,
        connection,
        Sender.ELASTIC,
    )
    process_runner(redis, listener_to_sender)


def process_runner(redis: Redis, listener_to_sender: ListenerToSender) -> None:
    schedule.every(ProcessEnvs.TIME_INTERVAL).minutes.do(
        calculate_unfinished_sortie, redis, listener_to_sender
    )
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
