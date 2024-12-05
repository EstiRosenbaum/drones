import base64
import io
import math
from typing import Any, Callable, List, Tuple

import flet as ft
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

from server.config import Config
from server.location import Location
from server.map import Map
from UI.controls.container import Container
from UI.controls.image import Img
from UI.controls.mouse_event_layer import MouseEventLayer

matplotlib.use("svg")


COLOR = List[int]
IMAGE = None


class Renderer:
    RED: COLOR = [255, 0, 0]
    GREEN: COLOR = [0, 255, 0]
    BLUE: COLOR = [0, 0, 255]

    def __init__(self, config: Config):
        self.config = config

    @staticmethod
    def print_map_with_painted_dots(geo_map: Map, dots: List[Location], color: COLOR):
        image = Renderer.create_rgb_image(geo_map)
        Renderer.paint_dots(image, dots, color)
        Renderer.print(image)

    @staticmethod
    def _get_neighborhood(
        geo_map: Map, x: int, y: int, radius: int
    ) -> List[Tuple[int, int]]:
        dots = []
        n, m = geo_map.nparray.shape
        for i in range(max(0, x - radius - 1), min(x + radius + 1, n)):
            for j in range(max(0, y - radius - 1), min(y + radius + 1, m)):
                if math.sqrt((i - x) ** 2 + (j - y) ** 2) < radius:
                    dots.append((i, j))
        return dots

    @staticmethod
    def _dot_size(value, a, b) -> int:
        rate = (value - a) / b
        return int(5 + rate * 45)

    @staticmethod
    def create_rgb_image(geo_map: Map):
        min_value = geo_map.nparray.min()
        # max_value = max(geo_map.nparray.max(), self.config.height_buffer_from_ground[1])
        max_value = geo_map.nparray.max()
        scaled = (geo_map.nparray - min_value) / (max_value - min_value)
        image = (scaled * 255).astype(np.uint8)
        return np.dstack((image, image, image))

    @staticmethod
    def paint_dots(image, dots: List[Location], color):
        for dot in dots:
            image[dot.i, dot.j] = color

    @staticmethod
    def print(image):
        plt.imshow(image)
        plt.axis("off")
        plt.show()

    @staticmethod
    def print_on_hover(
        image: np.ndarray, page: ft.Page, on_hover: Callable[[Any], None] = None
    ) -> None:
        def convert_nparray_to_bytes(image: np.ndarray) -> str:
            img = Image.fromarray(image, "RGB")
            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format="PNG")
            img_byte_array = img_byte_array.getvalue()

            return base64.b64encode(img_byte_array).decode("utf-8")

        def hover_on_image(e: ft.HoverEvent) -> None:
            point_info.value = on_hover(e)
            point_info.update()

        global IMAGE

        if IMAGE is not None:
            page.controls.remove(IMAGE)
            page.controls.pop()

        point_info = ft.Text("")
        container = Container(point_info, height=100)
        base64_string = convert_nparray_to_bytes(image)
        image = Img(src_base64=base64_string)
        IMAGE = MouseEventLayer(
            mouse_cursor=ft.MouseCursor.CLICK, on_hover=hover_on_image, content=image
        )

        page.add(container)
        page.add(IMAGE)
        page.update()
