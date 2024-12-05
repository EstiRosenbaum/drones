import math
from typing import List

import pandas as pd

from modules.setup_env import get_env_instance
from server.config import Config
from server.map import Map
from server.route import Route
from server.s3_api.s3_actions import save_csv_file
from server.utils.logger.w_logger import logger


class HeightsTable:
    ROUTE_POINT_NUMBER_HEADER = "מס״ד נקודה"
    DISTANCE_HEADER = "מרחק"
    CUMULATIVE_DISTANCE_HEADER = "מרחק מצטבר"
    GROUND_HEIGHT_HEADER = "גובה קרקע מעפ״י (מטר)"
    PLATFORM_HEIGHT_FROM_GROUND = "גובה מטוס מעפ״ש (מטר)"
    PLATFORM_HEIGHT_FROM_SEA = "גובה מטוס מעפ״י (מטר)"

    HEADER_ROW = [
        ROUTE_POINT_NUMBER_HEADER,
        DISTANCE_HEADER,
        CUMULATIVE_DISTANCE_HEADER,
        GROUND_HEIGHT_HEADER,
        PLATFORM_HEIGHT_FROM_GROUND,
        PLATFORM_HEIGHT_FROM_SEA,
    ]

    def __init__(self, config: Config, route: Route, geo_map: Map):
        self.config: Config = config
        self.route: Route = route
        self.map: Map = geo_map

    def parse_csv(self) -> List[List[str]]:
        csv_data = [list(self.HEADER_ROW)]
        cumulative_distance = 0
        landmark_point = 1
        distance = 0
        for i in range(len(self.route.geolocations)):
            distance += (
                self.route.geolocations[i]
                .calc_distance(self.route.geolocations[i - 1])
                .kilometers
                if i != 0
                else 1
            )

            if not self.route.geolocations[i].landmark:
                continue

            row = [landmark_point]
            landmark_point += 1

            row.append(round(distance, 1))
            cumulative_distance += distance
            distance = 0
            row.append(round(cumulative_distance, 1))

            ground_height = self.map.get_height(
                self.route.geolocations[i].get_indices()
            )
            row.append(self.normalize(ground_height))

            height_from_ground = self.route.geolocations[i].get_height() - ground_height
            row.append(self.normalize(height_from_ground))

            height = self.route.geolocations[i].get_height()
            row.append(self.normalize(height))

            row = list(row)
            csv_data.append(row)

        return csv_data

    def save_csv(self, csv_data: List[List[str]]) -> None:
        table_file_name = f"{self.config.route_name}-table.csv"
        data = pd.DataFrame(csv_data)
        bucket_name = get_env_instance().BUCKET_NAME

        save_csv_file(data, bucket_name, table_file_name)
        logger.info("Finished generate")

    @staticmethod
    def normalize(n):
        return math.ceil(n / 50) * 50
