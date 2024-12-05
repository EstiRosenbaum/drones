import flet as ft


class Container(ft.Container):
    def __init__(
        self,
        content: ft.Control,
        height: int | float = None,
        width: int | float = None,
        padding=None,
    ) -> None:
        super().__init__()
        self.content = content
        self.height = height
        self.width = width
        self.padding = padding
