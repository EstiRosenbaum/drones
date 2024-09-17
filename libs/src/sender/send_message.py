from helpers.logger.w_logger import logger
from sender.sender_factory import get_sender


class SendMessage:
    def __init__(self, sender_type: str) -> None:
        self.sender = get_sender(sender_type)

    def send_message(self, message: object, index: str, type: str) -> None:
        message = {**message, "index": index, "type": type}
        try:
            self.sender.send_message(message)
        except Exception as error:
            logger.error(f"Failed during sending message to {index} - {error}.")
