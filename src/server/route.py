from typing import List, Tuple

from bresenham import bresenham

from server.config import Config
from server.geolocation import Geolocation
from server.location import Location
from server.map import Map
from server.parse_to_geolocations import (
    parse_control_point_to_geolocation,
    parse_geolocations_from_route_input,
)


class Route:
    def __init__(self, config: Config):
        self.config: Config = config
        self.geolocations: List[Geolocation] = []
        self.landmarks: List[int] = []
        self.x_boundaries: Tuple[int, int] = None
        self.y_boundaries: Tuple[int, int] = None
        self.control_geolocation: Geolocation = None

    def init(self) -> "Route":
        self.geolocations = parse_geolocations_from_route_input(
            self.config.type, self.config.route, find_duplications=True
        )
        self.control_geolocation = parse_control_point_to_geolocation(
            self.config.control_point
        )
        self._set_geolocation_heights_based_on_landmarks(self.geolocations)
        self._set_route_map_boundaries()

        return self

    def pair(self, geo_map: Map):
        n = len(self.geolocations)
        for i in range(n):
            geolocation: Geolocation = self.geolocations[i]
            self._pair_geolocations_with_indices(geolocation, geo_map)
        self._pair_geolocations_with_indices(self.control_geolocation, geo_map)

    def get_routing_points(self, geo_map: Map) -> List[List[Location]]:
        routing_points: List[List[Location]] = []
        n = len(self.geolocations)
        routing_points.append([self.geolocations[0].to_location()])
        resolution = geo_map.meters_to_index_distance(
            self.config.routing_points_resolution
        )
        for i in range(n - 1):
            p1, p2 = (
                self.geolocations[i],
                self.geolocations[i + 1],
            )
            routing_points[-1] += self._generate_points_between_two_landmarks(
                p1, p2, resolution
            )
            routing_points.append([p2.to_location()])
        return routing_points

    def get_possible_locations(self, geo_map: Map) -> List[Location]:
        route_dots: List[Location] = []
        location_index = 0
        next_location = self._create_landmark_point(geo_map, location_index)
        radius = geo_map.meters_to_index_distance(self.config.location_error_radius)
        while location_index < len(self.geolocations) - 1:
            i, j, h, takeoff, landing = (
                next_location.i,
                next_location.j,
                next_location.h,
                next_location.takeoff,
                next_location.landing,
            )
            route_dots += geo_map.get_neighborhood(next_location, radius)
            next_location = self._create_landmark_point(geo_map, location_index)
            line = list(bresenham(i, j, next_location.i, next_location.j))
            n = len(line)
            for i in range(n):
                point = line[i]
                step_size = (1 + i) / n
                height = h + step_size * (next_location.h - h)
                middle_point = Location(point[0], point[1], height, takeoff, landing)
                route_dots += geo_map.get_neighborhood(middle_point, radius)
            location_index += 1
        return route_dots

    def get_control_geolocation(self):
        return self.control_geolocation

    def get_geolocations(self) -> List[Geolocation]:
        return self.geolocations

    def _set_geolocation_heights_based_on_landmarks(self, landmarks: List[Geolocation]):
        assert (
            len(landmarks) > 0
        ), "landmarks should be initialized before setting geolocation heights"

        i = 0
        last_h = None
        for landmark in landmarks:
            while i < len(self.geolocations):
                distance = landmark.calc_distance(self.geolocations[i]).meters
                if distance <= self.config.geographic_precision_in_meters:
                    last_h = landmark.z
                    self.geolocations[i].z = landmark.z
                    self.geolocations[i].landmark = True
                    self.landmarks.append(i)
                    if len(self.landmarks) == 0:
                        self.geolocations[i].takeoff_point = True
                    i += 1
                    break
                elif i == 0:
                    raise ValueError(
                        "first geolocation should match between routing points and landmarks"
                    )
                else:
                    self.geolocations[i].z = last_h
                    i += 1

        if len(self.landmarks) != len(landmarks):
            msg = f"found {len(self.landmarks)} landmark points out of {len(landmarks)}. please check:"
            msg += (
                "\n1. landmark points exists in the route file (a point in the routing file should be equal"
                " or close enough to the landmark point)"
            )
            msg += (
                f"\n2. landmark point no. {len(self.landmarks)} appears before landmark point "
                f"no. {len(self.landmarks) + 1} in the route file."
            )
            raise ValueError(msg)

        self.geolocations[self.landmarks[-1]].landing_point = True

    def _create_landmark_point(self, geo_map: Map, index: int) -> Location:
        x, y, z = self.geolocations[index].get_geo_3d()
        next_i, next_j = geo_map.get_index_by_utm_coordinates(x, y)
        return Location(
            next_i,
            next_j,
            z,
            takeoff=(index == 0),
            landing=(index == len(self.geolocations) - 2),
        )

    def _set_route_map_boundaries(self):
        assert (
            self.control_geolocation
        ), "control point should be initialized before setting up the map boundaries"
        min_x, max_x = self.control_geolocation.x, self.control_geolocation.x
        min_y, max_y = self.control_geolocation.y, self.control_geolocation.y

        for loc in self.geolocations:
            min_x, max_x = min(min_x, loc.x), max(max_x, loc.x)
            min_y, max_y = min(min_y, loc.y), max(max_y, loc.y)

        self.x_boundaries = (float(min_x), float(max_x))
        self.y_boundaries = (float(min_y), float(max_y))

    @staticmethod
    def _generate_points_between_two_landmarks(
        p1: Geolocation, p2: Geolocation, resolution: int
    ) -> List[Location]:
        ps: List[Location] = []
        generated_points = list(bresenham(p1.i, p1.j, p2.i, p2.j))
        for i in range(1 + resolution, len(generated_points) - 2, 1 + resolution):
            p = generated_points[i]
            ps.append(
                Location(
                    p[0], p[1], p1.z, p1.takeoff_point, p1.landing_point, landmark=False
                )
            )
        return ps

    @staticmethod
    def _pair_geolocations_with_indices(geolocation: Geolocation, geo_map: Map):
        x, y = geolocation.get_geo_2d()
        i, j = geo_map.get_index_by_utm_coordinates(x, y)
        geolocation.set_indices(i, j)
