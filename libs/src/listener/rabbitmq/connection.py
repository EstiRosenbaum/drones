import pika
from helpers.logger.w_logger import logger
from helpers.utils.const import RabbitMQconnection


def Connection() -> pika.BlockingConnection:
    try:
        connnection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RabbitMQconnection.HOST, port=RabbitMQconnection.PORT
            )
        )
        logger.info("Successfully connected to RabbitMQ.")
        return connnection
    except Exception as error:
        logger.critical(f"Error creating connection to RabbitMQ - {error}.")
