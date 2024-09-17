import json

from listener_to_sender.listener_to_sender import ListenerToSender


def test_init(
    patch_get_listener,
    patch_MessageManagement,
    queue_name,
    listener_type,
    mock_connection,
    sender_type,
):
    with patch_get_listener as get_listener, patch_MessageManagement as messageManagement:
        result = ListenerToSender(
            queue_name, listener_type, mock_connection, sender_type
        )
        assert result.queue_name == queue_name
        assert result.service_name == queue_name
        get_listener.assert_called()
        messageManagement.assert_called()


def test_queue_listener(listener_to_sender_instance, mock_get_listener):
    listener_to_sender_instance.queue_listener()
    mock_get_listener.consume.assert_called_once()


def test_message_received_callback(
    listener_to_sender_instance,
    message,
    patch_process_message,
    patch_post_process_message,
    patch_save_message,
    processed_message,
):
    with patch_process_message as _process_message, patch_post_process_message as _post_process_message, patch_save_message as save_message:
        listener_to_sender_instance.message_received_callback(message)
        _process_message.assert_called_with(message)
        _post_process_message.assert_called_with(processed_message)
        save_message.assert_called_with(processed_message)


def test_process_message(listener_to_sender_instance, message):
    new_message_processor = listener_to_sender_instance._process_message(message)
    assert new_message_processor == json.loads(message)
