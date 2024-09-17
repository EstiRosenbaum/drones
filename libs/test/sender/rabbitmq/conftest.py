from unittest.mock import MagicMock, Mock, patch

import pytest


@pytest.fixture
def queue_name():
    return "test-queue"


@pytest.fixture
def channel():
    return Mock()


@pytest.fixture
def message(obj):
    return obj


@pytest.fixture
def EnumExchangeDEFAULT():
    from helpers.utils.const import RabbitMQExchange

    return RabbitMQExchange.DEFAULT.value


@pytest.fixture
def RabbitMQSender_instance(queue_name, mock_connection):
    from sender.rabbitmq.rabbitmq_sender import RabbitMQSender

    return RabbitMQSender(mock_connection, queue_name)


@pytest.fixture
def current_path():
    return "sender.rabbitmq.rabbitmq_sender"


@pytest.fixture
def patch_logger(current_path):
    return patch(f"{current_path}.logger", Mock())


@pytest.fixture
def connection(queue_name, channel):
    connection = MagicMock()
    connection.channel.return_value = channel
    return {"connection": connection, "queue_name": queue_name}
