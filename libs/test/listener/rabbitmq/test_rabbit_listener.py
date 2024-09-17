from helpers.utils.const import RabbitMQ
from listener.rabbitmq.rabbit_listener import RabbitMQListener


def test_RabbitMQListener_initialization(
    queue_name,
    mock_callback,
    mock_connection,
    patch_definition_listens_queue,
    patch_definition_dead_letter_queue,
):
    with patch_definition_listens_queue as definition_listens, patch_definition_dead_letter_queue as definition_dead_letter:
        RabbitMQListener_instance = RabbitMQListener(
            queue_name, mock_connection, callback=mock_callback
        )
        assert RabbitMQListener_instance.queue_name == queue_name
        assert isinstance(RabbitMQListener_instance.channel, object)
        RabbitMQListener_instance.channel.queue_declare.assert_not_called()
        assert RabbitMQListener_instance.consume_message_callback == mock_callback
        definition_listens.assert_called_once()
        definition_dead_letter.assert_called_once()


def test_exception_handling(
    patch_logger,
    queue_name,
    mock_connection,
    mock_callback,
    Exception_message,
    exception,
):
    with exception, patch_logger as mock_logger:
        RabbitMQListener(queue_name, mock_connection, callback=mock_callback)
        mock_logger.error.assert_called_once_with(
            f"Error initializing rabbitMQListener: {Exception_message}"
        )


def test_consumer(RabbitMQListener_instance, patch_logger, queue_name):
    with patch_logger as logger_errors:
        RabbitMQListener_instance.consume()
        assert isinstance(RabbitMQListener_instance.channel, object)
        assert hasattr(RabbitMQListener_instance.channel, "basic_qos")
        RabbitMQListener_instance.channel.basic_qos.assert_called_once_with(
            prefetch_count=1
        )
        assert hasattr(RabbitMQListener_instance.channel, "basic_consume")
        logger_errors.info.assert_called_with(
            f"Start consuming from {queue_name} queue"
        )
        assert hasattr(RabbitMQListener_instance.channel, "start_consuming")
        logger_errors.error.assert_not_called()


def test_consumer_exception_handling(
    patch_logger,
    queue_name,
    RabbitMQListener_instance,
    Exception_message,
    mock_start_consuming,
):
    with patch_logger as mock_logger, mock_start_consuming as mock_basic_consume:
        mock_basic_consume.side_effect = Exception(Exception_message)
        RabbitMQListener_instance.consume()
        mock_logger.info.assert_called_with(f"Start consuming from {queue_name} queue")
        mock_logger.error.assert_called_once_with(
            f"Error consuming message: {Exception_message}"
        )


def test_callback(
    RabbitMQListener_instance, patch_logger, mock_arg_callback, patch_retry_callback
):
    ch, method, properties, body = mock_arg_callback
    with patch_logger as patch_logger, patch_retry_callback:
        RabbitMQListener_instance._callback(ch, method, properties, body)
        RabbitMQListener_instance._retry_callback.assert_called_once_with(body.decode())
        ch.basic_ack.assert_called_with(delivery_tag=method.delivery_tag)
        patch_logger.assert_not_called()


def test_callback_exception_handling(
    RabbitMQListener_instance,
    patch_logger,
    mock_arg_callback,
    exception,
    patch_retry_callback,
):
    ch, method, properties, body = mock_arg_callback
    with exception, patch_logger as patch_logger, patch_retry_callback:
        RabbitMQListener_instance._callback(ch, method, properties, body)
        RabbitMQListener_instance._retry_callback.assert_called_once_with(body.decode())
        patch_logger.error.assert_called_once_with(
            "Error consume message: Simulated error"
        )
        ch.basic_nack.assert_called_with(
            delivery_tag=method.delivery_tag, requeue=False
        )


def test_declare_queue(RabbitMQListener_instance, queue_name, routing_key, direct_name):
    RabbitMQListener_instance.declare_queue()
    RabbitMQListener_instance.channel.queue_declare.assert_called_with(
        queue=queue_name,
        durable=True,
        arguments={
            "x-dead-letter-exchange": direct_name,
            "x-dead-letter-routing-key": routing_key,
        },
    )


def test_declare_dead_letter_queue(
    RabbitMQListener_instance,
    dead_letter_queue,
    routing_key,
    direct_name,
    ExchangeDIRECT,
):
    RabbitMQListener_instance.declare_dead_letter_queue()
    RabbitMQListener_instance.channel.exchange_declare.assert_called_with(
        exchange=direct_name, exchange_type=ExchangeDIRECT
    )
    RabbitMQListener_instance.channel.queue_declare.assert_called_with(
        queue=dead_letter_queue
    )
    RabbitMQListener_instance.channel.queue_bind.assert_called_with(
        queue=dead_letter_queue,
        exchange=direct_name,
        routing_key=routing_key,
    )


def test_retry_attempts(RabbitMQListener_instance, message, exception):
    with exception as error:
        RabbitMQListener_instance._retry_callback(message)
        assert error.last_attempt.attempt_number == RabbitMQ.RETRY
