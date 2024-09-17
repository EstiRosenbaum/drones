from typing import Any

from helpers.logger.w_logger import logger
from helpers.utils.const import RabbitMQ, RabbitMQExchange
from listener.listener import Listener
from pika import BlockingConnection
from tenacity import retry, stop_after_attempt, wait_fixed


class RabbitMQListener(Listener):
    def __init__(
        self, queue_name: str, connection: BlockingConnection, callback: Any
    ) -> None:
        try:
            self.queue_name = queue_name
            self.channel = connection.channel()
            self.declare_queue()
            self.declare_dead_letter_queue()
            self.consume_message_callback = callback
        except Exception as e:
            logger.error(f"Error initializing rabbitMQListener: {e}")

    def declare_queue(self) -> None:
        self.channel.queue_declare(
            queue=self.queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": RabbitMQ.DIRECT_NAME,
                "x-dead-letter-routing-key": f"{RabbitMQ.ROUTING_START}_{self.queue_name}",
            },
        )

    def declare_dead_letter_queue(self) -> None:
        dead_letter_queue = f"{RabbitMQ.DEAD_QUEUE_START}_{self.queue_name}"
        self.channel.exchange_declare(
            exchange=RabbitMQ.DIRECT_NAME, exchange_type=RabbitMQExchange.DIRECT
        )
        self.channel.queue_declare(queue=dead_letter_queue)
        self.channel.queue_bind(
            queue=dead_letter_queue,
            exchange=RabbitMQ.DIRECT_NAME,
            routing_key=f"{RabbitMQ.ROUTING_START}_{self.queue_name}",
        )

    def consume(self) -> None:
        try:
            logger.info(f"Start consuming from {self.queue_name} queue")
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue=self.queue_name, on_message_callback=self._callback, auto_ack=True
            )
            self.channel.start_consuming()
        except Exception as e:
            logger.error(f"Error consuming message: {e}")

    def _callback(self, ch: Any, method: Any, properties: Any, body: Any) -> None:
        message = body.decode()
        try:
            self._retry_callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Error consume message: {e.last_attempt.exception()}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    @retry(
        stop=stop_after_attempt(RabbitMQ.RETRY),
        wait=wait_fixed(RabbitMQ.WAIT_BEFORE_RETRY),
    )
    def _retry_callback(self, message):
        self.consume_message_callback(message)
