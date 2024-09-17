from functools import partial
from typing import Any

import pyproj
import utm
from helpers.logger.w_logger import logger
from shapely.geometry import Polygon
from shapely.ops import transform, unary_union


def get_area_in_meters(footprints: list) -> float:
    if len(footprints) == 0:
        return 0.0
    try:
        polygons = []
        zone_number = utm.latlon_to_zone_number(
            footprints[0][0][0], footprints[0][0][1]
        )
        for footprint in footprints:
            polygon = Polygon(footprint)
            polygons.append(polygon)
        merged_polygon = unary_union(polygons)
        merged_polygon = convert_polygon_to_utm(merged_polygon, zone_number)
        return merged_polygon.area
    except Exception as e:
        logger.error(f"Error during area calculation: {str(e)}")


def get_area_in_km(footprints: list) -> float:
    return get_area_in_meters(footprints) / 1e6


def convert_polygon_to_utm(polygon: list, zone_number: int) -> Any:
    transformer = pyproj.Transformer.from_crs("epsg:4326", f"epsg:326{zone_number}")
    proj = partial(transformer.transform)
    new_polygon = transform(proj, polygon)
    return new_polygon
