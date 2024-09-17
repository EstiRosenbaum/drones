from unittest.mock import Mock, patch

import pytest
from helpers.utils.const import Listener, Sender
from modules.classes_activating_process import (
    _create_instance,
    _extracting_classes_details,
    _filter_py_files,
    classes_activating_process,
)


@pytest.fixture
def file_name():
    return "file_test.py"


@pytest.fixture
def class_name():
    return "FileTest"


@pytest.fixture
def module_name():
    return "file_test"


@pytest.fixture
def sortie_module():
    return "sortie_module"


@pytest.fixture
def other_module():
    return "other_module"


@pytest.fixture
def python_files():
    return ["try_file1.py", "try_file2.py"]


@pytest.fixture
def class_files(python_files):
    return [*python_files, "try_file3.js"]


@pytest.fixture
def args(mock_module, mock_connection):
    return [mock_module, "TestClass", mock_connection]


@pytest.fixture
def args_class(mock_connection):
    return Listener.RABBITMQ, mock_connection, Sender.ELASTIC


@pytest.fixture
def mock_instance():
    return Mock()


@pytest.fixture
def mock_redis(mock_instance):
    return mock_instance


@pytest.fixture
def mock_connection(mock_instance):
    return mock_instance


@pytest.fixture
def mock_module(mock_instance):
    return mock_instance


@pytest.fixture
def basic_path():
    return "modules.classes_activating_process"


@pytest.fixture
def patch_extracting_classes_details(basic_path):
    return patch(
        f"{basic_path}._extracting_classes_details",
        return_value=["module_name", "module", "class_name"],
    )


@pytest.fixture
def patch_create_instance(basic_path):
    return patch(f"{basic_path}._create_instance")


@pytest.fixture
def patch_importlib(basic_path, mock_instance):
    return patch(
        f"{basic_path}.importlib.import_module",
        return_value=mock_instance,
    )


@pytest.fixture
def patch_filter_py_files(basic_path, python_files):
    return patch(
        f"{basic_path}._filter_py_files",
        return_value=python_files,
    )


def test_classes_activating_process(
    class_files,
    patch_extracting_classes_details,
    patch_create_instance,
    patch_filter_py_files,
    mock_redis,
    mock_connection,
):
    with patch_filter_py_files as filter_py_files, patch_extracting_classes_details as extracting_classes_details, patch_create_instance as create_instance:
        classes_activating_process(class_files, mock_connection, mock_redis)
        filter_py_files.assert_called_with(class_files)
        extracting_classes_details.assert_called()
        assert extracting_classes_details.call_count == len(
            filter_py_files.return_value
        )
        create_instance.assert_called()
        assert create_instance.call_count == len(filter_py_files.return_value)


def test_filter_py_files(class_files, python_files):
    files = _filter_py_files(class_files)
    assert list(files) == python_files


def test_extracting_classes_details(
    file_name, class_name, module_name, patch_importlib, mock_instance
):
    with patch_importlib:
        module_names, module, class_names = _extracting_classes_details(file_name)
        assert (
            class_names == class_name
            and module_names == module_name
            and module == mock_instance
        )


def test_create_instance_with_redis(
    args, args_class, sortie_module, mock_module, mock_redis
):
    _create_instance(sortie_module, *args, mock_redis)

    mock_module.TestClass.assert_called_with(sortie_module, *args_class, mock_redis)
    mock_module.TestClass.return_value.queue_listener.assert_called_once()


def test_create_instance_without_redis(args, args_class, other_module, mock_module):
    _create_instance(other_module, *args, None)

    mock_module.TestClass.assert_called_with(other_module, *args_class)
    mock_module.TestClass.return_value.queue_listener.assert_called_once()
