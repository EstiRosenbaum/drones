from .send_message import SendMessage


class MessageManagement:
    def __init__(self, sender_type: str) -> None:
        self.sender = SendMessage(sender_type)

    def send_message(self, message: object, index: str, type: str = "create") -> None:
        self.sender.send_message(message, index, type)
