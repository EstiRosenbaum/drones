import flet as ft


def update_status(status, page: ft.Page, status_value: str) -> None:
    status.value = status_value
    page.update()
