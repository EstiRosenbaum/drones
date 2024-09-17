import json
from typing import Self

from helpers.logger.w_logger import logger
from helpers.utils.const import RabbitMQExchange
from pika import BlockingConnection
from sender.sender import Sender


class RabbitMQSender(Sender):
    def __init__(self, connection: BlockingConnection, queue_name: str) -> None:
        self.queue_name = queue_name
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    @classmethod
    def create_connection(cls: Self, connection: object) -> Self:
        return cls(connection.get("connection"), connection.get("queue_name"))

    def send_message(self, message: object) -> None:
        try:
            self.channel.basic_publish(
                exchange=RabbitMQExchange.DEFAULT.value,
                routing_key=self.queue_name,
                body=json.dumps(message),
            )
        except Exception as e:
            logger.error(f"Error publish message: {e}")

    def _check_connection(self) -> bool:
        pass
