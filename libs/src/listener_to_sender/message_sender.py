from sender.message_management import MessageManagement


class MessageSender:
    def __init__(
        self,
        index_name: str,
        sender_type: str,
    ) -> None:
        self.service_name = index_name
        self.service = MessageManagement(sender_type)

    def save_message(self, processed_message: object, index: str = None) -> None:
        self.service.send_message(
            {"message": processed_message}, index or self.service_name
        )

    def update_message(
        self, message: object, identifiers: object, index: str = None
    ) -> None:
        self.service.send_message(
            {"message": message, "identifiers": identifiers},
            index or self.service_name,
            "update",
        )
