import threading
import time
from collections import defaultdict, deque
from typing import Any, Callable, Deque, Dict, List, Set, Tuple

import flet as ft

from server.config import Config
from server.converters import Converters
from server.heights import Heights
from server.heights_table import HeightsTable
from server.location import Location
from server.map import Map
from server.renderer import Renderer
from server.route import Route
from server.utils.logger.w_logger import logger


class Validator:
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]
    PURPLE = [128, 0, 128]

    def __init__(
        self,
        config: Config,
        route: Route,
        heights: Heights,
        geo_map: Map,
        renderer: Renderer,
        heights_table: HeightsTable,
    ):
        self.config = config
        self.route = route
        self.heights = heights
        self.map = geo_map
        self.renderer = renderer
        self.heights_table = heights_table

    def validate(self, page: ft.Page, stop_event: threading.Event) -> str:
        image = self.renderer.create_rgb_image(self.map)
        los_violations: List[str] = []
        height_violations: List[str] = []
        sqr_radius = (
            self.map.meters_to_index_distance(self.config.location_error_radius) ** 2
        )
        n, m = self.map.nparray.shape
        visited: Set[Tuple[int, int]] = set()
        queue: Deque[Location] = deque()
        routing_points: List[List[Location]] = self.route.get_routing_points(self.map)
        routing_points_map: Dict[Tuple[int, int], Tuple[float, int]] = {}
        leg_number = 0
        for leg in routing_points:
            for p in leg:
                if p.landmark:
                    leg_number += 1

                queue.append((p, p, leg_number))

        while queue:
            if stop_event.is_set():
                return "Timeout occurred during command execution"
            loc, center, leg_number = queue.popleft()
            i, j = loc.i, loc.j

            if i < 0 or i == n or j < 0 or j == m:
                continue

            if (i, j) in visited:
                continue
            visited.add((i, j))

            if (center.i - i) ** 2 + (center.j - j) ** 2 > sqr_radius:
                continue

            routing_points_map[(loc.i, loc.j)] = loc.h, leg_number
            self.paint_violations(image, los_violations, height_violations, loc)

            neighbors: List[Tuple[int, int]] = [
                (i + 1, j),
                (i - 1, j),
                (i, j + 1),
                (i, j - 1),
            ]
            for n in neighbors:
                neighbor = Location(n[0], n[1], loc.h, loc.takeoff, loc.landing)
                queue.append((neighbor, center, leg_number))

        threading.Thread(
            target=lambda: self._print_violations(los_violations, height_violations)
        ).start()
        Renderer.print_on_hover(
            image, page, on_hover=self._on_hover(routing_points_map)
        )
        return "Completed!"

    def _on_hover(
        self, routing_points_map: Dict[Tuple[int, int], Tuple[float, int]]
    ) -> Callable[[Any], None]:
        def on_hover(e: ft.HoverEvent) -> str | None:
            time.sleep(0.1)
            column = int(e.local_x)
            row = int(e.local_y)
            current_point = (row, column)

            if current_point in routing_points_map:
                ground_height = self.map.get_height(current_point)
                allowed_height = self.heights.get(current_point)
                current_height, leg_number = routing_points_map[current_point]
                return f"Heights:\nground: {int(ground_height)}\nmin los: {int(allowed_height)} \nroute: {int(current_height)}\nleg: {leg_number}"

            return ""

        return on_hover

    def generate(self, stop_event: threading.Event) -> str:
        sqr_radius = (
            self.map.meters_to_index_distance(self.config.location_error_radius) ** 2
        )
        n, m = self.map.nparray.shape
        queue: Deque = deque()
        routing_points: List[List[Location]] = self.route.get_routing_points(self.map)
        center_min_possible_height = defaultdict(float)
        landmark_point = None
        visited = set()
        for leg in routing_points:
            for p in leg:
                if p.landmark:
                    landmark_point = p.i, p.j
                    visited = set()

                if not landmark_point:
                    raise Exception("First routing point has to be a landmark point")

                queue.append((p, p, landmark_point, visited))
        while queue:
            if stop_event.is_set():
                return "Timeout occurred during command execution"
            loc, center, leg_starting_point, visited = queue.popleft()
            p = i, j = loc.i, loc.j

            if i < 0 or i == n or j < 0 or j == m:
                continue

            if (i, j) in visited:
                continue
            visited.add((i, j))

            if (center.i - i) ** 2 + (center.j - j) ** 2 > sqr_radius:
                continue

            allowed_height = (
                self.heights.get(p) + self.config.los_safety_distance_below_platform + 1
            )
            ground_height = (
                self.map.get_height(p)
                + self.config.min_distance_from_surface_height
                + 1
            )
            center_min_possible_height[leg_starting_point] = max(
                center_min_possible_height[leg_starting_point],
                allowed_height,
                ground_height,
            )

            neighbors: List[Tuple[int, int]] = [
                (i + 1, j),
                (i - 1, j),
                (i, j + 1),
                (i, j - 1),
            ]
            for n in neighbors:
                neighbor = Location(n[0], n[1], loc.h, loc.takeoff, loc.landing)
                queue.append((neighbor, center, leg_starting_point, visited))

        for geolocation in self.route.geolocations:
            geolocation.z = center_min_possible_height[geolocation.get_indices()]

        csv_data = self.heights_table.parse_csv()
        self.heights_table.save_csv(csv_data)
        return "Completed!"

    def paint_violations(
        self,
        image,
        los_violations: List[str],
        height_violations: List[str],
        loc: Location,
    ):
        p = (loc.i, loc.j)
        allowed_height = self.heights.get(p)
        ground_height = self.map.get_height(p)

        surface_violation = False
        los_violation = False
        if loc.h <= ground_height + self.config.min_distance_from_surface_height:
            surface_violation = True
            height_violations.append(
                self._get_height_violation_message_format(loc, ground_height)
            )

        if loc.h <= allowed_height + self.config.los_safety_distance_below_platform:
            los_violation = True
            los_violations.append(
                self._get_los_violation_message_format(loc, allowed_height)
            )

        self._paint_violation(image, loc.i, loc.j, los_violation, surface_violation)

    def _paint_violation(self, image, i: int, j: int, los: bool, surface: bool):
        current_los, current_surface = self._current_violations(image, i, j)

        los = los or current_los
        surface = surface or current_surface

        if los and surface:
            color = self.PURPLE
        elif los:
            color = self.RED
        elif surface:
            color = self.BLUE
        else:
            color = self.GREEN

        image[i, j] = color

    def _current_violations(self, image, i, j) -> Tuple[bool, bool]:
        color = image[i, j].tolist()
        los = color in (self.RED, self.PURPLE)
        surface = color in (self.BLUE, self.PURPLE)
        return los, surface

    @staticmethod
    def validate_route_geolocations_above_ground_height(
        geo_map: Map, route: Route, print_detailed_results: bool
    ) -> bool:
        result = True
        for geolocation in route.get_geolocations():
            x, y, z = geolocation.get_geo_3d()
            i, j = geo_map.get_index_by_utm_coordinates(x, y)
            ground_height = geo_map.get_height((i, j))

            if z <= ground_height:
                if not print_detailed_results:
                    return False

                lat, lng = Converters.to_latlng(x, y)
                logger.error(
                    f"illegal height on ({lat},{lng}): {z} (ground height: {ground_height})"
                )
                result = False

        return result

    @staticmethod
    def _print_violations(los: List[str], ground: List[str]):
        for g in ground:
            logger.info(g)

        for i in los:
            logger.info(i)

    def _get_los_violation_message_format(
        self, loc: Location, allowed_height: float
    ) -> str:
        x, y = self.map.get_utm_coordinates_by_index(loc.i, loc.j)
        return f"{x},{y} violates los restriction ({int(loc.h)} < {int(allowed_height) + 1} + {self.config.los_safety_distance_below_platform})"

    def _get_height_violation_message_format(
        self, loc: Location, ground_height: float
    ) -> str:
        x, y = self.map.get_utm_coordinates_by_index(loc.i, loc.j)
        return f"{x},{y} violates minimum height limitation ({int(loc.h)} < {int(ground_height) + 1} + {self.config.min_distance_from_surface_height})"
