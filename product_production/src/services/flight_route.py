import json

from data_processors.data_process_functions import process_date, process_geo_line
from listener_to_sender.listener_to_sender import ListenerToSender


class FlightRoute(ListenerToSender):
    def _process_message(self, message: str) -> object:
        message = json.loads(message)
        message["Date"] = process_date(message["Date"])
        message["Waypoints"] = process_geo_line(message["Waypoints"])
        return message
