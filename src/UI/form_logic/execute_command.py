import threading
import time

import flet as ft

from modules.setup_env import get_env_instance
from server.command import generate_3d_command, validate_route_command
from server.initialization.config import create_config
from UI.form_logic.helpers import update_status
from UI.form_logic.validation import is_valid

execution_lock = threading.Lock()
current_thread = None
stop_event = threading.Event()


def start_execution_thread(
    dict_default_value_controls: dict, dict_controls: dict, page: ft.Page
) -> None | str:
    global current_thread

    if not check_is_valid(dict_controls):
        return "Input Format Violation. aborted..."

    with execution_lock:
        if current_thread and current_thread.is_alive():
            return "Execution blockage - another process is running. This may take a few minutes; please wait and click again."

        current_thread = threading.Thread(
            target=execute, args=(dict_default_value_controls, dict_controls, page)
        )
        current_thread.start()


def check_is_valid(dict_controls: dict) -> bool:
    include_height = True if dict_controls["type"] == "validate" else False
    return is_valid(
        dict_controls["control_point"],
        dict_controls["route_path"],
        dict_controls["route_name"],
        include_height,
    )


def execute(
    dict_default_value_controls: dict,
    dict_controls: dict,
    page: ft.Page,
) -> None | str:
    global stop_event
    stop_event.clear()
    config = create_config(dict_controls, page)

    if not config:
        return "Internal Error: failed to parse config file"

    timer_thread = threading.Timer(
        int(get_env_instance().LOCK_TIME), timeout_handler, [stop_event]
    )
    timer_thread.start()

    try:
        if dict_controls["type"] == "validate":
            command = validate_route_command(config, page, stop_event)
        else:
            command = generate_3d_command(config, dict_controls["download"], stop_event)

        update_status(dict_controls["status"], page, command)
        time.sleep(4)
        clean_controls(dict_controls, dict_default_value_controls, page)

    except Exception:
        update_status(
            dict_controls["status"],
            page,
            "Internal Error: Exception occurred during command execution",
        )
        time.sleep(4)
        clean_controls(dict_controls, dict_default_value_controls, page)

    finally:
        timer_thread.cancel()


def timeout_handler(stop_event: threading.Event) -> None:
    stop_event.set()


def clean_controls(
    dict_controls: dict, dict_default_value_controls: dict, page: ft.Page
) -> None:
    for control in dict_controls:
        if not isinstance(dict_controls[control], str):
            dict_controls[control].value = dict_default_value_controls[control]
            page.update()
