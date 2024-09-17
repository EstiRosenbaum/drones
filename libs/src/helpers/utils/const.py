import os
from enum import Enum


class RabbitMQconnection:
    HOST = os.getenv("RABBITMQ_HOST")
    PORT = os.getenv("RABBITMQ_PORT")


class Listener:
    RABBITMQ = "rabbitMQ"


class Sender:
    ELASTIC = "ElasticSearch"
    RABBITMQ = "RabbitMq"


class RabbitMQExchange(Enum):
    DEFAULT = ""
    DIRECT = "direct"
    FANOUT = "fanout"
    HEADERS = "headers"
    TOPIC = "topic"


class State(Enum):
    CREATE = "created"
    UPDATE = "updated"


class RabbitMQ:
    DEAD_QUEUE_START = "dead_letter"
    ROUTING_START = "dead"
    DIRECT_NAME = "direct_log"
    RETRY = 5
    WAIT_BEFORE_RETRY = 2
