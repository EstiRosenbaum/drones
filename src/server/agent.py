import threading

import flet as ft

from server.config import Config
from server.heights import Heights
from server.heights_table import HeightsTable
from server.location import Location
from server.map import Map
from server.renderer import Renderer
from server.route import Route
from server.utils.logger.w_logger import logger
from server.validator import Validator


class Agent:
    def __init__(self, config: Config):
        self.config: Config = config
        self.geo_map: Map = None
        self.route: Route = None
        self.route_map: Map = None
        self.heights: Heights = None
        self.renderer = None
        self.validator = None
        self.heights_table = None
        self._initialized: bool = False

    def init(self, validate_route_heights: bool = True) -> "Agent":
        self.geo_map = Map(self.config).init()
        self.renderer = Renderer(self.config)
        if self.set_route(self.config.route, validate_route_heights) is None:
            return
        self.heights_table = HeightsTable(self.config, self.route, self.route_map)
        self.validator = Validator(
            self.config,
            self.route,
            self.heights,
            self.route_map,
            self.renderer,
            self.heights_table,
        )

        self._initialized = True
        return self

    def set_route(self, route_path, validate_route_heights: bool) -> "Config":
        self.config.set_route_path(route_path)

        self.route = Route(self.config).init()
        if (
            validate_route_heights
            and not Validator.validate_route_geolocations_above_ground_height(
                self.geo_map, self.route, True
            )
        ):
            return None

        self.pair_route_and_map()
        self.heights = Heights(
            self.config, self.route_map, self.route.get_control_geolocation()
        ).init()
        return self

    def generate_heights_to_routing_points(self):
        assert self._initialized, "agent should be initialized before any operation"
        pass

    def print_route(self):
        assert self._initialized, "agent should be initialized before any operation"
        dots = self.route.get_possible_locations(self.route_map)
        self.renderer.print_map_with_painted_dots(self.route, dots, Renderer.RED)

    def print_heights_map(self):
        assert self._initialized, "agent should be initialized before any operation"
        i, j, z = self.heights.control_point.get_indices_3d()
        padding = self.route_map.meters_to_index_distance(
            self.config.location_error_radius
        )
        dots = self.heights.heights_map.get_neighborhood(Location(i, j, z), padding)
        self.renderer.print_map_with_painted_dots(
            self.heights.heights_map, dots, Renderer.RED
        )

    def validate_route(self, page: ft.Page, stop_event: threading.Event):
        logger.info("Start validate")
        return self.validator.validate(page, stop_event)

    def generate_3d_route(self, stop_event: threading.Event):
        logger.info("Start generate")
        return self.validator.generate(stop_event)

    def create_smaller_tif_file(self):
        x_boundaries = [499052, 899999]
        y_boundaries = [3004490, 3883090]
        Map(self.config).init().focus(x_boundaries, y_boundaries).save(
            "server/artifacts/israel.tif"
        )

    def initialized(self):
        return self._initialized

    def pair_route_and_map(self):
        self.route_map = self.geo_map.focus(
            self.route.x_boundaries, self.route.y_boundaries
        )
        self.route.pair(self.route_map)
