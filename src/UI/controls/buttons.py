from typing import Optional

import flet as ft


class Button(ft.ElevatedButton):
    DEFAULT_WIDTH = 300
    DEFAULT_HEIGHT = 35

    def __init__(
        self,
        text: Optional[str],
        on_click,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        disabled=False,
    ) -> None:
        super().__init__()
        self.text = text
        self.on_click = on_click
        self.width = width
        self.height = height
        self.disabled = disabled


class PopUpButton(ft.TextButton):
    def __init__(self, text: str, on_click) -> None:
        super().__init__()
        self.text = text
        self.on_click = on_click


class IconButton(ft.IconButton):
    def __init__(
        self,
        icon: ft.icons,
        on_click,
        icon_color=None,
        tooltip=None,
        visible: bool = True,
    ) -> None:
        super().__init__()
        self.icon = icon
        self.tooltip = tooltip
        self.on_click = on_click
        self.icon_color = icon_color
        self.visible = visible
