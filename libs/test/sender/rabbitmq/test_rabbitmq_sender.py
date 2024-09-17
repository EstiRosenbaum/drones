import json
from unittest.mock import Mock

from sender.rabbitmq.rabbitmq_sender import RabbitMQSender


def test_RabbitMQSender_initialization(RabbitMQSender_instance, queue_name):
    assert RabbitMQSender_instance.queue_name == queue_name
    assert isinstance(RabbitMQSender_instance.channel, object)
    assert hasattr(RabbitMQSender_instance.channel, "queue_declare")
    RabbitMQSender_instance.channel.queue_declare.assert_called_once_with(
        queue=queue_name, durable=True
    )


def test_create_connection_success(connection, channel, queue_name):
    sender = RabbitMQSender.create_connection(connection)
    assert isinstance(sender, RabbitMQSender)
    assert sender.queue_name == queue_name
    assert sender.channel == channel


def test_producer_publish_successful(
    message, RabbitMQSender_instance, EnumExchangeDEFAULT
):
    RabbitMQSender_instance.channel.basic_publish = Mock()
    RabbitMQSender_instance.send_message(message)
    RabbitMQSender_instance.channel.basic_publish.assert_called_once_with(
        exchange=EnumExchangeDEFAULT,
        routing_key=RabbitMQSender_instance.queue_name,
        body=json.dumps(message),
    )


def test_producer_publish_error(
    message,
    RabbitMQSender_instance,
    patch_logger,
    error_message_publish,
    mock_error_send_message,
):
    with patch_logger as logger_error:
        RabbitMQSender_instance.channel.basic_publish = mock_error_send_message
        RabbitMQSender_instance.send_message(message)
        logger_error.error.assert_called_once_with(
            f"Error publish message: {error_message_publish}"
        )
