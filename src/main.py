import asyncio

import flet as ft
import schedule

from server.utils.logger.d_logger import delete_old_logs_files
from UI.load_flet.display_controls import main


async def process_runner():
    schedule.every().day.do(delete_old_logs_files)

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


def start():
    loop = asyncio.get_event_loop()
    loop.create_task(process_runner())
    loop.create_task(continue_process())
    loop.run_forever()


def continue_process():
    ft.app(target=main, web_renderer=ft.WebRenderer.HTML)


if __name__ == "__main__":
    start()
