import json
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def queue_name():
    return "test-queue"


@pytest.fixture
def index():
    return "test-index"


@pytest.fixture
def listener_type():
    return "rabbitMQ"


@pytest.fixture
def sender_type():
    return "ElasticSearch"


@pytest.fixture
def message():
    return json.dumps({"message": "Test message"})


@pytest.fixture
def processed_message():
    return "processed test message"


@pytest.fixture
def identifiers():
    return "Test identifiers"


@pytest.fixture
def listener_to_sender_instance(
    queue_name,
    listener_type,
    mock_connection,
    sender_type,
    patch_get_listener,
    patch_MessageManagement,
    mock_env,
):
    with mock_env:
        from listener_to_sender.listener_to_sender import ListenerToSender

        with patch_get_listener, patch_MessageManagement:
            return ListenerToSender(
                queue_name, listener_type, mock_connection, sender_type
            )


@pytest.fixture
def message_sender_instance(
    queue_name,
    sender_type,
    patch_MessageManagement,
):
    from listener_to_sender.message_sender import MessageSender

    with patch_MessageManagement:
        return MessageSender(queue_name, sender_type)


@pytest.fixture
def current_path():
    return "listener_to_sender.listener_to_sender"


@pytest.fixture
def message_sender_path():
    return "listener_to_sender.message_sender"


@pytest.fixture
def class_path(current_path):
    return f"{current_path}.ListenerToSender"


@pytest.fixture
def patch_get_listener(current_path, mock_get_listener):
    return patch(f"{current_path}.get_listener", return_value=mock_get_listener)


@pytest.fixture
def patch_MessageManagement(message_sender_path, mock_MessageManagement):
    return patch(
        f"{message_sender_path}.MessageManagement", return_value=mock_MessageManagement
    )


@pytest.fixture
def patch_process_message(class_path, processed_message):
    return patch(
        f"{class_path}._process_message",
        return_value=processed_message,
    )


@pytest.fixture
def patch_post_process_message(class_path):
    return patch(f"{class_path}._post_process_message")


@pytest.fixture
def patch_save_message(class_path):
    return patch(f"{class_path}.save_message")


@pytest.fixture
def mock_connection():
    return "connection"


@pytest.fixture
def mock_process_message(processed_message):
    return Mock(return_value=processed_message)


@pytest.fixture
def mock_get_listener():
    return Mock()


@pytest.fixture
def mock_MessageManagement():
    return Mock()
