from typing import List, Tuple

from server.converters import Converters
from server.geolocation import Geolocation

HEIGHT = 3000


def parse_geolocations_from_route_input(
    type: str, route: str, find_duplications: bool = False
) -> List[Geolocation]:
    geolocations = []
    for point_line in route.split("\n"):
        point = point_line.split(" , ")
        x, y = Converters.from_latlng(float(point[1]), float(point[0]))
        geolocation = create_geolocation_point_by_type(type, x, y, point)
        geolocations.append(geolocation)

    if find_duplications:
        msg, duplications = find_duplicated_landmarks(geolocations)
        if duplications:
            raise ValueError("error0000", msg)

    return geolocations


def create_geolocation_point_by_type(
    type: str, x: float, y: float, point: list[str]
) -> Geolocation:
    if type == "validate" and len(point) > 2:
        return create_geolocation_point(x, y, float(point[2]))
    else:
        return create_geolocation_point(x, y, float(HEIGHT))


def create_geolocation_point(x: float, y: float, z: float) -> Geolocation:
    return Geolocation(x, y, z)


def parse_control_point_to_geolocation(control_point):
    x, y = Converters.from_latlng(control_point[1], control_point[0])
    return create_geolocation_point(x, y, control_point[2])


def find_duplicated_landmarks(landmarks: List[Geolocation]) -> Tuple[str, bool]:
    visited = {}
    for i in range(len(landmarks)):
        p = (landmarks[i].x, landmarks[i].y)
        if p in visited:
            return f"duplication found: row no. {visited[p] + 1} and {i+1}", True
        visited[p] = i

    return "", False
