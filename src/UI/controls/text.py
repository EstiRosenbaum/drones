from typing import Optional

import flet as ft


class Text(ft.Text):
    def __init__(
        self,
        text: str,
        weight: Optional[ft.FontWeight],
        text_align: Optional[ft.TextAlign],
        size: Optional[int],
    ):
        super().__init__()
        self.value = text
        self.weight = weight
        self.text_align = text_align
        self.size = size
