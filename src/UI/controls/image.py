import flet as ft


class Img(ft.Image):
    def __init__(self, src_base64: str, width=None, height=None) -> None:
        super().__init__()
        self.src_base64 = src_base64
        self.width = width
        self.height = height
