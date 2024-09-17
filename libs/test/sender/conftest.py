from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def type():
    return "create"


@pytest.fixture
def index():
    return "test-index"


@pytest.fixture
def service():
    return "test-service"


@pytest.fixture
def current_path():
    return "sender.send_message"


@pytest.fixture
def error_message_publish():
    return "Publish error"


@pytest.fixture
def obj():
    return {"key": "value"}


@pytest.fixture
def message(index, obj):
    return {"message": obj, "index": index}


@pytest.fixture
def sender_rabbitMQ():
    return "RabbitMq"


@pytest.fixture
def sender_elastic():
    return "ElasticSearch"


@pytest.fixture
def type_sender(sender_elastic):
    return sender_elastic


@pytest.fixture
def type_sender_invalid():
    return "test-invalid-type"


@pytest.fixture
def es_instance():
    return Mock()


@pytest.fixture
def patch_elasticSearch(es_instance):
    return patch(
        "sender.elastic.elastic_message_sender.Elasticsearch",
        return_value=es_instance,
    )


@pytest.fixture
def patch_elastic(es_instance):
    return patch(
        "sender.elastic.elastic_sender.ElasticSender.create_connection",
        return_value=es_instance,
    )


@pytest.fixture
def patch_rabbitmq(es_instance):
    return patch(
        "sender.rabbitmq.rabbitmq_sender.RabbitMQSender.create_connection",
        return_value=es_instance,
    )


@pytest.fixture
def patch_sender(es_instance):
    sender_mock = es_instance
    return patch("sender.send_message.get_sender", return_value=sender_mock)


@pytest.fixture
def patch_sender_error():
    return patch(
        "sender.sender_factory.get_sender", side_effect=Exception("example-error")
    )


@pytest.fixture
def patch_send_message(es_instance):
    send_message_mock = es_instance
    return patch(
        "sender.message_management.SendMessage", return_value=send_message_mock
    )


@pytest.fixture
def patch_logger(current_path):
    return patch(f"{current_path}.logger", Mock())


@pytest.fixture
def mock_error_send_message(error_message_publish):
    return Mock(side_effect=Exception(error_message_publish))


@pytest.fixture
def mock_sender():
    return "elastcsearch"


@pytest.fixture
def mock_connection():
    return Mock(return_value={"host": "localhost", "port": "5672"})
