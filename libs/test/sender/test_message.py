def test_send_message(patch_sender, es_instance, type_sender, message, index, type):
    with patch_sender:
        from sender.send_message import SendMessage

        send_message = SendMessage(type_sender)
        send_message.send_message(message, index, type)
        send_message.sender.send_message.assert_called_once_with(
            {**message, "index": index, "type": type}
        )
    assert send_message.sender == es_instance


def test_send_message_error(patch_sender, type_sender, message, index, type, exception):
    with exception, patch_sender:
        from sender.send_message import SendMessage

        send_message = SendMessage(type_sender)
        send_message.sender.send_message = exception(message)
        send_message.send_message(message, index, type)
