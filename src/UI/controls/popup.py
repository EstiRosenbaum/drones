import flet as ft

from UI.controls.text import Text


class PopUp(ft.AlertDialog):
    def __init__(self, title, content, actions, modal=True) -> None:
        super().__init__()
        self.modal = modal
        if isinstance(title, str):
            self.title = Text(title, ft.FontWeight.NORMAL, ft.TextAlign.CENTER, 20)
        else:
            self.title = title
        self.content = content
        self.actions = actions
        self.actions_alignment = ft.MainAxisAlignment.END
