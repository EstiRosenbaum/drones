from listener.listener_factory import RabbitMQListener, get_listener


def test_get_listener_with_valid_type(
    patch_RabbitMQListener, listener_type, queue_name, mock_connection, mock_callback
):
    with patch_RabbitMQListener:
        listener = get_listener(
            listener_type, queue_name, mock_connection, mock_callback
        )
        assert isinstance(listener, RabbitMQListener)


def test_get_listener_with_invalid_type(
    invalid_listener_type, queue_name, mock_connection, mock_callback
):
    listener = get_listener(
        invalid_listener_type, queue_name, mock_connection, mock_callback
    )
    assert listener is None
