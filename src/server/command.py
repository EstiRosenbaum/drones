import threading

import flet as ft

from server.agent import Agent
from server.config import Config
from server.utils.logger.w_logger import logger
from UI.controls.buttons import Button


def validate_route_command(
    config: Config, page: ft.Page, stop_event: threading.Event
) -> str | None:
    try:
        agent = Agent(config).init()
        if not agent:
            logger.error("Internal Error: failed to initialize the agent")
            return "Internal Error: failed to initialize the agent"

        result = agent.validate_route(page, stop_event)
        return result
    except ValueError as err:
        return str(err)
    except Exception:
        logger.error(
            "Internal Error: exception occurred while running validate command"
        )
        return "Internal Error: exception occurred while running validate command"


def generate_3d_command(
    config: Config, download: Button, stop_event: threading.Event
) -> None | str:
    try:
        agent = Agent(config).init()
        if not agent:
            logger.error("Internal Error: failed to initialize the agent")
            return "Internal Error: failed to initialize the agent"
        result = agent.generate_3d_route(stop_event)
        if result == "Completed!":
            download.visible = True
        return result
    except ValueError as err:
        return str(err)
    except Exception as err:
        logger.error(
            f"Internal Error: exception occurred while running generate 3d command - {err}"
        )
        return "Internal Error: exception occurred while running generate 3d command"
