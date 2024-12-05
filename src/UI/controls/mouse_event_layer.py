import flet as ft


class MouseEventLayer(ft.GestureDetector):
    def __init__(
        self, mouse_cursor: ft.MouseCursor, on_hover, content: ft.ControlEvent
    ) -> None:
        super().__init__()
        self.mouse_cursor = mouse_cursor
        self.on_hover = on_hover
        self.content = content
