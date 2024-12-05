import math
from typing import Dict, Tuple

import numpy as np
from bresenham import bresenham

from server.config import Config
from server.geolocation import Geolocation
from server.map import Map


class Heights:
    EARTH_CURVATURE_ANGLE = 0.5
    EARTH_CURVATURE_MULTIPLIER = math.tan(EARTH_CURVATURE_ANGLE)

    def __init__(self, config: Config, geo_map: Map, control_point: Geolocation):
        self.config: Config = config
        self.map: Map = geo_map
        self.heights_map: Map = self.map.clone_structure()
        self.control_point: Geolocation = control_point
        self.gradients: Dict[Tuple[int, int], float] = {}
        self.should_consider_earth_curvature = False

    def init(self) -> "Heights":
        cp_height = min(
            self.control_point.get_height(),
            self.map.get_height(self.control_point.get_indices()),
        )
        self.heights_map.set_height(self.control_point.get_indices(), cp_height)

        lines = []
        cp = self.control_point
        n, m = self.map.nparray.shape
        for i in range(0, n):
            lines.append(list(bresenham(cp.get_i(), cp.get_j(), i, 0)))
            lines.append(list(bresenham(cp.get_i(), cp.get_j(), i, m - 1)))

        for i in range(0, m):
            lines.append(list(bresenham(cp.get_i(), cp.get_j(), 0, i)))
            lines.append(list(bresenham(cp.get_i(), cp.get_j(), n - 1, i)))

        for line in lines:
            self.calculate_height(line)

        return self

    def get(self, point: Tuple[int, int]) -> float:
        return self.heights_map.get_height(point)

    def calculate_height(self, line):
        current_gradient = -float("inf")
        n = len(line)
        current_height = None
        for i in range(1, n):
            self.maybe_consider_earth_curvature(line, i)
            current_height, current_gradient = self.get_los_height(
                line[i - 1], line[i], current_height, current_gradient
            )
            self.heights_map.set_height(line[i], current_height)

    def maybe_consider_earth_curvature(self, line, i):
        if self.should_consider_earth_curvature:
            return

        cp_height_respecting_earth_curvature = (
            self.control_point.get_height()
            - i * math.dist(line[i], line[i - 1]) * self.EARTH_CURVATURE_MULTIPLIER
        )
        if cp_height_respecting_earth_curvature <= self.map.get_height(line[i]):
            self.should_consider_earth_curvature = True

    def get_los_height(
        self,
        prev_point: Tuple[int, int],
        current_point: Tuple[int, int],
        current_height: float,
        current_gradient: float,
    ):
        h = self.map.get_height(current_point)
        pi, pj = current_point
        if current_point in self.gradients.keys():
            gradient = self.gradients[current_point]
        else:
            gradient = self.calculate_gradient(
                self.control_point.get_indices_3d(), (pi, pj, h)
            )
            self.gradients[current_point] = self.calc_safe_gradient(gradient)

        if gradient > current_gradient:
            current_gradient = gradient
            current_height = h + self.config.los_safety_distance_above_peak
        else:
            current_height += current_gradient * math.dist(current_point, prev_point)

        return current_height, current_gradient

    def calc_safe_gradient(self, gradient: bool):
        angle = self.config.los_safety_angle
        if self.should_consider_earth_curvature:
            angle += self.EARTH_CURVATURE_ANGLE

        if angle == 0:
            return gradient

        tan = np.tan(math.radians(angle))
        return (tan + gradient) / (1 - tan * gradient)

    @staticmethod
    def calculate_gradient(p1: Tuple[int, int, float], p2: Tuple[int, int, float]):
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        sign = -1 if z1 < 0 and z2 < 0 else 1
        return sign * ((z2 - z1) / math.dist((x1, y1), (x2, y2)))
