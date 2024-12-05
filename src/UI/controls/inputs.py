from typing import Any

import flet as ft


class Input(ft.TextField):
    def __init__(
        self,
        label: str,
        value: str = "",
        read_only: bool = False,
        helper_text: str = "",
        width: int = 250,
        data: Any = None,
    ):
        super().__init__()
        self.label = label
        self.value = value
        self.width = width
        self.read_only = read_only
        self.helper_text = helper_text
        self.data = data


class InputNumber(Input):
    def __init__(self, label: str, value: int = 0):
        super().__init__(label)
        self.input_filter = ft.InputFilter(
            allow=True, regex_string=r"^(0|[1-9][0-9]*)?$"
        )
        self.value = value


class InputTextArea(Input):
    def __init__(self, label: str, helper_text: str = "") -> None:
        super().__init__(label)
        self.shift_enter = True
        self.multiline = True
        self.min_lines = 11
        self.max_lines = 11
        self.helper_text = helper_text
        self.text_vertical_align = ft.VerticalAlignment.START
