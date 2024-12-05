from typing import Tuple

from geopy.distance import Distance, geodesic

from server.converters import Converters
from server.location import Location


class Geolocation:
    def __init__(self, utm_x: float, utm_y: float, z: float = None):
        self.x: float = utm_x
        self.y: float = utm_y
        self.z: float = z
        self.i: int = None
        self.j: int = None
        self.target: bool = False
        self.takeoff_point: bool = False
        self.landing_point: bool = False
        self.landmark: bool = False

    def set_indices(self, i: int, j: int):
        self.i = i
        self.j = j

    def get_geo_3d(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z

    def get_indices_3d(self) -> Tuple[int, int, float]:
        return self.i, self.j, self.z

    def get_geo_2d(self) -> Tuple[float, float]:
        return self.x, self.y

    def get_indices(self) -> Tuple[int, int]:
        return self.i, self.j

    def get_height(self) -> float:
        return self.z

    def get_i(self):
        return self.i

    def get_j(self):
        return self.j

    def is_target(self) -> bool:
        return self.target

    def to_location(self) -> Location:
        return Location(
            self.i,
            self.j,
            self.z,
            self.takeoff_point,
            self.landing_point,
            self.landmark,
        )

    def calc_distance(self, geolocation: "Geolocation") -> Distance:
        l1 = Converters.to_latlng(geolocation.x, geolocation.y)
        l2 = Converters.to_latlng(self.x, self.y)
        return geodesic(l1, l2)
