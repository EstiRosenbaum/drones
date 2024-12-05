import math
from typing import List, Tuple

import numpy as np
import tifffile as tif
from numpy import ndarray

from server.config import Config
from server.location import Location


class Map:
    def __init__(self, config: Config):
        self.dataset = None
        self.nparray: ndarray = None
        self.origin: Tuple[float, float] = None
        self.pixel_width: Tuple[float, float] = None
        self.scale_factor: float = None
        self.config: Config = config
        self.focused = False

    def init(self) -> "Map":
        self.scale_factor = 2
        self.nparray = tif.imread("/app/map.tif")
        # self.origin = (101847.74705442542, 4669568.987782747)
        self.origin = (441494, 3845296)
        self.pixel_width = (11, -11)
        return self

    def focus(
        self, x_boundaries: Tuple[float, float], y_boundaries: Tuple[float, float]
    ):
        assert self.nparray is not None, "map is not initialized"
        xi, yi = self.get_index_by_utm_coordinates(x_boundaries[0], y_boundaries[1])
        xj, yj = self.get_index_by_utm_coordinates(x_boundaries[1], y_boundaries[0])
        self.origin = x_boundaries[0], y_boundaries[1]
        n, m = self.nparray.shape[1], self.nparray.shape[0]
        padding = self.meters_to_index_distance(self.config.map_padding)
        self.nparray = self.nparray[
            max(0, xi - padding) : min(xj + padding, m),
            max(0, yi - padding) : min(yj + padding, n),
        ]
        self.focused = True
        return self

    def clone_structure(self) -> "Map":
        clone = Map(self.config)
        clone.dataset = self.dataset
        clone.nparray = np.zeros(self.nparray.shape)
        clone.origin = self.origin
        clone.pixel_width = self.pixel_width
        clone.scale_factor = self.scale_factor
        return clone

    def get_index_by_utm_coordinates(self, x: float, y: float) -> Tuple[int, int]:
        assert self.origin is not None, "map is not initialized"
        i = self.meters_to_index_distance(self.origin[1] - y)
        j = self.meters_to_index_distance(x - self.origin[0])

        map_padding = (
            self.meters_to_index_distance(self.config.map_padding)
            if self.focused
            else 0
        )
        return i + map_padding, j + map_padding

    def get_utm_coordinates_by_index(self, i, j) -> Tuple[float, float]:
        assert self.origin is not None, "map is not initialized"
        map_padding = (
            self.meters_to_index_distance(self.config.map_padding)
            if self.focused
            else 0
        )
        i -= map_padding
        j -= map_padding

        y = self.origin[1] - self.index_distance_to_meters(i)
        x = self.origin[0] + self.index_distance_to_meters(j)

        return y, x

    def get_neighborhood(self, loc: Location, radius: int) -> List[Location]:
        dots: List[Location] = []
        n, m = self.nparray.shape
        for i in range(max(0, loc.i - radius - 1), min(loc.i + radius + 1, n)):
            for j in range(max(0, loc.j - radius - 1), min(loc.j + radius + 1, m)):
                if math.sqrt((i - loc.i) ** 2 + (j - loc.j) ** 2) < radius:
                    dots.append(Location(i, j, loc.h, loc.takeoff, loc.landing))
        return dots

    def get_height(self, point: Tuple[int, int]) -> float:
        return self.nparray[point[0], point[1]]

    def set_height(self, point: Tuple[int, int], height: float):
        self.nparray[point[0], point[1]] = height

    def meters_to_index_distance(self, meters: int) -> int:
        return int(meters / (self.pixel_width[0] * self.scale_factor))

    def index_distance_to_meters(self, distance: int):
        return distance * self.pixel_width[0] * self.scale_factor

    def save(self, path):
        tif.imwrite(path, self.nparray)
