from typing import Tuple

import utm

from server.utils.logger.w_logger import logger


class Converters:
    UTM_ZONE_NUMBER = 36
    UTM_ZONE_LETTER = "N"

    @staticmethod
    def to_latlng(utm_easting: float, utm_northing: float) -> Tuple[float, float]:
        lat, lng = utm.to_latlon(
            utm_easting,
            utm_northing,
            Converters.UTM_ZONE_NUMBER,
            Converters.UTM_ZONE_LETTER,
        )
        return lat, lng

    @staticmethod
    def from_latlng(lat: float, lng: float) -> Tuple[float, float]:
        try:
            easting, northing, _, _ = utm.from_latlon(
                lat,
                lng,
                force_zone_number=Converters.UTM_ZONE_NUMBER,
                force_zone_letter=Converters.UTM_ZONE_LETTER,
            )
            return easting, northing

        except ValueError as err:
            if Converters.is_valid_utm_coords(lat, lng):
                return lat, lng

            if Converters.is_valid_utm_coords(lng, lat):
                return lng, lat

            raise err

    @staticmethod
    def is_valid_utm_coords(x, y) -> bool:
        result = False
        try:
            Converters.to_latlng(x, y)
            result = True
            logger.info("Utm coords is valid")
        except ValueError:
            result = False
            logger.error("Utm coords is not valid")
        finally:
            return result
