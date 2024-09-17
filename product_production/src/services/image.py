import json

from data_processors.data_process_functions import (
    extracting_time_properties,
    process_dates,
    process_geo_point,
)
from listener_to_sender.listener_to_sender import ListenerToSender
from utils.const import Indexes


class Image(ListenerToSender):
    def _process_message(self, message: str) -> object:
        message = json.loads(message)
        message = process_dates(message)
        message["Sensor_Position"] = process_geo_point(message["Sensor_Position"])
        return message

    def _post_process_message(self, message: object) -> None:
        times_message = extracting_time_properties(message)
        identifiers = {"Photo_time": message["Photo_time"]}
        self.update_message(times_message, Indexes.DATES, identifiers)
