import math
from typing import List, Tuple

import numpy as np
import tifffile as tif

from server.config import Config


class GeoImage:
    def __init__(self, config: Config, origin: Tuple[int, int], pixel_width: int):
        self.config = config
        self.image_data: np.ndarray = None
        self.origin: Tuple[float, float] = origin
        self.scale_factor: int = pixel_width * 2
        self.padding = 0

    def init(self):
        self.image_data: np.ndarray = tif.imread("/app/map.tif")

    def clone(self) -> "GeoImage":
        d = self.get_dimensions()
        image = GeoImage(self.config, self.origin, self.scale_factor / 2)
        image.padding = self.padding
        image.image_data = np.zeros(d[1], d[0])
        return image

    def focus(
        self, x_boundaries: Tuple[float, float], y_boundaries: Tuple[float, float]
    ):
        self.origin = x_boundaries[0], y_boundaries[1]
        self.padding = p = self._meters_to_indices(self.config.map_padding)

        # not worried too much about IndexOutOfBound. this system assumes our map is very large.
        top_left = x_boundaries[0] - p, y_boundaries[1] + p
        bottom_right = x_boundaries[1] + p, y_boundaries[0] - p
        self.image_data = self._get_box(top_left, bottom_right)

    def get(self, c: Tuple[float, float]) -> float:
        return self._get(self._to_indices(c))

    def get_neighborhood(self, c: Tuple[float, float], radius_in_meters: int):
        p = self._to_indices(c)
        dots: List[Tuple[float, float, float]] = []
        n, m = self.get_dimensions()
        radius = radius_in_meters  # FIXME
        for i in range(max(0, p[0] - radius), min(p[0] + radius, n)):
            for j in range(max(0, p[1] - radius), min(p[1] + radius, m)):
                if math.sqrt((i - p[0]) ** 2 + (j - p[1]) ** 2) < radius:
                    neighbor = self._to_utm((i, j))
                    dots.append((neighbor[0], neighbor[1], self._get((i, j))))
        return dots

    def get_dimensions(self):
        return self.image_data.shape[1], self.image_data.shape[0]

    def _get_box(
        self, top_left: Tuple[float, float], bottom_right: Tuple[float, float]
    ) -> np.ndarray:
        tl, br = self._to_indices(top_left), self._to_indices(bottom_right)
        return self.image_data[br[1] : tl[1], tl[0] : br[0]]

    def _get(self, p: Tuple[int, int]) -> float:
        return self.image_data[p[0], p[1]]

    def _to_indices(self, c: Tuple[float, float]) -> Tuple[int, int]:
        return self._meters_to_indices(
            c[0] - self.origin[0]
        ) + self.padding, self._meters_to_indices(self.origin[1] - c[1]) + self.padding

    def _to_utm(self, p: Tuple[int, int]) -> Tuple[float, float]:
        return self.origin[1] - self._indices_to_meters(
            p[0] - self.padding
        ), self.origin[0] + self._indices_to_meters(p[1] - self.padding)

    def _meters_to_indices(self, meters: int) -> int:
        return int(meters / self.scale_factor)

    def _indices_to_meters(self, distance: int):
        return distance * self.scale_factor
