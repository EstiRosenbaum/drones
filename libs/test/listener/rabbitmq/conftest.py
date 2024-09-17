from unittest.mock import Mock, patch

import pytest
from helpers.utils.const import RabbitMQ, RabbitMQExchange


@pytest.fixture
def message():
    return "Test message"


@pytest.fixture
def Exception_message():
    return "mock exception"


@pytest.fixture
def dead_letter_queue(queue_name):
    return f"{RabbitMQ.DEAD_QUEUE_START}_{queue_name}"


@pytest.fixture
def routing_key(queue_name):
    return f"{RabbitMQ.ROUTING_START}_{queue_name}"


@pytest.fixture
def direct_name():
    return RabbitMQ.DIRECT_NAME


@pytest.fixture
def ExchangeDIRECT():
    return RabbitMQExchange.DIRECT


@pytest.fixture
def RabbitMQListener_instance(queue_name, mock_callback, mock_connection):
    from listener.rabbitmq.rabbit_listener import RabbitMQListener

    return RabbitMQListener(queue_name, mock_connection, callback=mock_callback)


@pytest.fixture
def current_path():
    return "listener.rabbitmq.rabbit_listener"


@pytest.fixture
def class_path(current_path):
    return f"{current_path}.RabbitMQListener"


@pytest.fixture
def path_connection_pika():
    return "listener.rabbitmq.connection.pika"


@pytest.fixture
def patch_ConnectionParameters(path_connection_pika, mock_connection):
    return patch(
        f"{path_connection_pika}.ConnectionParameters",
        return_value=mock_connection,
    )


@pytest.fixture
def patch_BlockingConnection(path_connection_pika, mock_connection):
    return patch(
        f"{path_connection_pika}.BlockingConnection",
        return_value=mock_connection,
    )


@pytest.fixture
def patch_definition_listens_queue(class_path):
    return patch(f"{class_path}.declare_queue")


@pytest.fixture
def patch_definition_dead_letter_queue(class_path):
    return patch(f"{class_path}.declare_dead_letter_queue")


@pytest.fixture
def patch_retry_callback(class_path):
    return patch(f"{class_path}._retry_callback")


@pytest.fixture
def patch_logger(current_path):
    return patch(f"{current_path}.logger", Mock())


@pytest.fixture
def mock_start_consuming(RabbitMQListener_instance):
    return patch.object(RabbitMQListener_instance.channel, "start_consuming")


@pytest.fixture
def mock_arg_callback():
    ch = Mock(return_value={"basic_nack": {}})
    method = Mock(return_value={"delivery_tag": "test_delivery_tag"})
    properties = {}
    body = b"Test message"
    return ch, method, properties, body


@pytest.fixture
def mock_Exception(Mock_instance):
    return Exception(Mock_instance)


@pytest.fixture
def mock_logger_info():
    return "Successfully connected to RabbitMQ."


@pytest.fixture
def mock_logger_error():
    return "Error creating connection to RabbitMQ"
