import importlib
from types import ModuleType

from helpers.utils.const import Listener, Sender
from listener.rabbitmq.connection import Connection
from redis_cache.connect_redis import Redis


def classes_activating_process(
    class_files: list[str], connection: Connection, redis: Redis
) -> None:
    python_files = _filter_py_files(class_files)
    for file in python_files:
        module_name, module, class_name = _extracting_classes_details(file)
        _create_instance(module_name, module, class_name, connection, redis)


def _filter_py_files(class_files):
    return filter(lambda file: file.endswith(".py"), class_files)


def _extracting_classes_details(file: str) -> tuple:
    module_name = file[:-3]
    module = importlib.import_module(f"services.{module_name}")
    class_name = "".join([word.capitalize() for word in module_name.split("_")])
    return module_name, module, class_name


def _create_instance(
    module_name: str,
    module: ModuleType,
    class_name: str,
    connection: Connection,
    redis: Redis,
) -> None:
    args = [module_name, Listener.RABBITMQ, connection, Sender.ELASTIC]

    if "sortie" in module_name or "end_systems" in module_name:
        class_instance = getattr(module, class_name)(*args, redis)
    else:
        class_instance = getattr(module, class_name)(*args)
    class_instance.queue_listener()
