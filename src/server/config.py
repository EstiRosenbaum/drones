from typing import Tuple


class Config:
    def __init__(self, route: str, type: str, route_name: str):
        self.route: str = route
        self.type: str = type
        self.route_name: str = route_name
        self.overview: int = 0
        self.control_point: Tuple[float, float, float] = None
        self.map_padding: int = 2000

        # route config
        self.location_error_radius: int = 0
        self.routing_points_resolution: int = 0
        self.min_distance_from_surface_height: int = 0
        self.los_safety_angle: int = 0
        self.los_safety_distance_below_platform: int = 0
        self.los_safety_distance_above_peak: int = 0
        self.geographic_precision_in_meters: int = 50

        # rl config
        self.height_max_limit: int = 3000
        self.elevation_rate: float = 0.1
        self.lowering_rate: float = 0.1

    def set_route_path(self, route: str) -> "Config":
        self.route = route
        return self

    def set_route_name(self, route_name: str) -> "Config":
        self.route_name = route_name
        return self

    def set_type(self, type: str) -> "Config":
        self.type = type
        return self

    def set_map_padding(self, padding: int) -> "Config":
        self.map_padding = padding
        return self

    def set_location_error_radius(self, radius: int) -> "Config":
        self.location_error_radius = radius
        return self

    def set_routing_points_resolution(self, resolution: int) -> "Config":
        self.routing_points_resolution = resolution
        return self

    def set_overview(self, overview: int) -> "Config":
        self.overview = overview
        return self

    def set_control_point(self, utm_x: float, utm_y: float, utm_z: float) -> "Config":
        self.control_point = (utm_x, utm_y, utm_z)
        return self

    def set_height_max_limit(self, limit: int) -> "Config":
        self.height_max_limit = limit
        return self

    def set_elevation_rate(self, rate: float) -> "Config":
        self.elevation_rate = rate
        return self

    def set_lowering_rate(self, rate: float) -> "Config":
        self.lowering_rate = rate
        return self

    def set_min_distance_from_surface_height(self, distance: int) -> "Config":
        self.min_distance_from_surface_height = distance
        return self

    def set_safety_angle_from_peak_los(self, angle: int) -> "Config":
        self.los_safety_angle = angle
        return self

    def set_safety_distance_below_platform(self, distance: int) -> "Config":
        self.los_safety_distance_below_platform = distance
        return self

    def set_safety_distance_above_peak(self, distance: int) -> "Config":
        self.los_safety_distance_above_peak = distance
        return self
