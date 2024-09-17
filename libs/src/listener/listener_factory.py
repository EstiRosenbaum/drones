from typing import Any

from helpers.utils.const import Listener
from listener.rabbitmq.rabbit_listener import RabbitMQListener
from pika import BlockingConnection


def get_listener(
    listener_type: str,
    queue_name: str,
    connection: BlockingConnection | None,
    callback: Any,
) -> Any | None:
    listeners = {Listener.RABBITMQ: RabbitMQListener}
    listener = listeners.get(listener_type)
    return None if listener is None else listener(queue_name, connection, callback)
