from unittest.mock import Mock, patch

import pytest
from helpers.utils.const import Listener, Sender
from utils.const import Indexes

from product_production.main import main


@pytest.fixture
def files_path():
    return "product_production/src/services"


@pytest.fixture
def basic_path():
    return "product_production.main"


@pytest.fixture
def mock_instance():
    return Mock()


@pytest.fixture
def patch_listdir(basic_path):
    return patch(f"{basic_path}.os.listdir")


@pytest.fixture
def patch_connection(basic_path, mock_instance):
    return patch(f"{basic_path}.Connection", return_value=mock_instance)


@pytest.fixture
def patch_redis(basic_path, mock_instance):
    return patch(f"{basic_path}.Redis", return_value=mock_instance)


@pytest.fixture
def patch_classes_activating_process(basic_path):
    return patch(f"{basic_path}.classes_activating_process")


@pytest.fixture
def patch_listener_to_sender(basic_path, mock_instance):
    return patch(f"{basic_path}.ListenerToSender", return_value=mock_instance)


@pytest.fixture
def patch_process_runner(basic_path):
    return patch(f"{basic_path}.process_runner")


def test_main(
    files_path,
    patch_listdir,
    patch_connection,
    patch_redis,
    patch_classes_activating_process,
    patch_listener_to_sender,
    patch_process_runner,
):
    with patch_listdir as listdir, patch_connection as connection, patch_redis as redis, patch_classes_activating_process as activating_process, patch_listener_to_sender as listener_to_sender, patch_process_runner as process_runner:
        main()
        listdir.assert_called_with(files_path)
        activating_process.assert_called_with(
            listdir.return_value, connection.return_value, redis.return_value
        )
        listener_to_sender.assert_called_with(
            Indexes.TAGGED_SORTIE,
            Listener.RABBITMQ,
            connection.return_value,
            Sender.ELASTIC,
        )
        process_runner.assert_called()


def test_delete_log_file(delete_log_file):
    pass
