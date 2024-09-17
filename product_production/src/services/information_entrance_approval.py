import json

from data_processors.data_process_functions import (
    extracting_time_properties,
    process_dates,
)
from listener_to_sender.listener_to_sender import ListenerToSender
from utils.const import Indexes


class InformationEntranceApproval(ListenerToSender):
    def _process_message(self, message: str) -> object:
        message = process_dates(json.loads(message))
        return message

    def _post_process_message(self, message: object) -> None:
        times_message = extracting_time_properties(message)
        identifiers = {"Photo_time": message["Photo_time"]}
        self.update_message(times_message, Indexes.DATES, identifiers)
