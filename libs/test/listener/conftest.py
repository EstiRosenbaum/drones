from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def queue_name():
    return "queue_test"


@pytest.fixture
def listener_type():
    return "rabbitMQ"


@pytest.fixture
def invalid_listener_type():
    return "invalid_type"


@pytest.fixture
def patch_RabbitMQListener():
    return patch("listener.rabbitmq.rabbit_listener.RabbitMQListener")


@pytest.fixture
def mock_connection():
    return Mock(return_value={"host": "localhost", "port": "5672"})


@pytest.fixture
def mock_callback():
    def callback_test():
        return "callback_test"

    return callback_test
