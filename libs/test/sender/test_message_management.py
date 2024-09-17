def test_send_message(
    patch_send_message, es_instance, type_sender, message, index, type
):
    with patch_send_message:
        from sender.message_management import MessageManagement

        message_management = MessageManagement(type_sender)
        message_management.send_message(message, index)
        message_management.sender.send_message.assert_called_once_with(
            message, index, type
        )
        assert message_management.sender == es_instance


def test_send_message_error(
    patch_logger, message, index, mock_error_send_message, exception
):
    with exception, patch_logger as logger_error:
        message_management = mock_error_send_message
        message_management.send_message(message, index)
        logger_error.error.assert_called()
