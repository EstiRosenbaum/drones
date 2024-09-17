from typing import Any

from helpers.utils.const import Sender
from sender.elastic.elastic_sender import ElasticSender
from sender.rabbitmq.rabbitmq_sender import RabbitMQSender


def get_sender(sender_type: str, connection: Any | None = None) -> Any | None:
    senders = {
        Sender.ELASTIC: ElasticSender,
        Sender.RABBITMQ: RabbitMQSender,
    }
    sender = senders.get(sender_type)
    return None if sender is None else sender.create_connection(connection)
