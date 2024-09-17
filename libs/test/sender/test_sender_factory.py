def test_get_sender_Elastic(
    patch_elastic,
    patch_rabbitmq,
    type_sender,
    mock_connection,
    es_instance,
):
    with patch_elastic, patch_rabbitmq:
        from sender.sender_factory import get_sender

        sender = get_sender(type_sender, mock_connection)
        assert sender == es_instance


def test_get_sender_Rabbit(
    patch_elastic,
    patch_rabbitmq,
    sender_rabbitMQ,
    mock_connection,
    es_instance,
):
    with patch_elastic, patch_rabbitmq:
        from sender.sender_factory import get_sender

        sender = get_sender(sender_rabbitMQ, mock_connection)
        assert sender == es_instance


def test_get_sender_invalid(
    patch_elastic, patch_rabbitmq, type_sender_invalid, mock_connection
):
    with patch_elastic, patch_rabbitmq:
        from sender.sender_factory import get_sender

        sender = get_sender(type_sender_invalid, mock_connection)
        assert sender is None
