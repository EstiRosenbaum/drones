from listener_to_sender.message_sender import MessageSender


def test_init(patch_MessageManagement, index, sender_type):
    with patch_MessageManagement as messageManagement:
        result = MessageSender(index, sender_type)
        assert result.service_name == index
        messageManagement.assert_called_with(sender_type)


def test_save_message(message_sender_instance, message, index, mock_MessageManagement):
    message_sender_instance.save_message(message, index)
    mock_MessageManagement.send_message.assert_called_once_with(
        {"message": message}, index
    )


def test_update_message(
    message_sender_instance, mock_MessageManagement, message, index, identifiers
):
    message_sender_instance.update_message(message, identifiers, index)
    mock_MessageManagement.send_message.assert_called_once_with(
        {"message": message, "identifiers": identifiers}, index, "update"
    )
