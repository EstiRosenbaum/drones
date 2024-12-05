import flet as ft

from UI.controls.text import Text


class ListTile(ft.ListTile):
    def __init__(
        self, text: str, weight: ft.FontWeight, text_align: ft.TextAlign, size: int
    ):
        super().__init__()
        self.title = Text(text, weight, text_align, size)
        self.justify_content = ft.MainAxisAlignment.CENTER
