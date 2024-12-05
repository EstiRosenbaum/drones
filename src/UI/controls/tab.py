from typing import List, Optional

import flet as ft


class Tab(ft.Tab):
    def __init__(
        self, content: ft.Control, icon: Optional[str], text: Optional[str]
    ) -> None:
        super().__init__()
        self.text = text
        self.icon = icon
        self.content = content


class Tabs(ft.Tabs):
    def __init__(
        self,
        on_click,
        tabs: List[Tab],
        height: int,
        selected_index: str = 0,
        animation_duration: str = 500,
        tab_alignment: ft.TabAlignment = ft.TabAlignment.START,
    ) -> None:
        super().__init__(
            tabs=tabs,
            height=height,
            selected_index=selected_index,
            animation_duration=animation_duration,
            tab_alignment=tab_alignment,
            on_change=on_click,
        )
