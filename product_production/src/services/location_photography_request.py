import json

from data_processors.data_process_functions import process_date, process_geo_shape
from listener_to_sender.listener_to_sender import ListenerToSender


class LocationPhotographyRequest(ListenerToSender):
    def _process_message(self, message: str) -> object:
        message = json.loads(message)
        message["Date"] = process_date(message["Date"])
        message["Footprint"] = process_geo_shape(message["Footprint"])
        return message
