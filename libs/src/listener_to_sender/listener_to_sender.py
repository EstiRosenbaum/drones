import json

from listener.listener_factory import get_listener
from pika import BlockingConnection

from listener_to_sender.message_sender import MessageSender


class ListenerToSender(MessageSender):
    def __init__(
        self,
        queue_name: str,
        listener_type: str,
        connection: BlockingConnection,
        sender_type: str,
    ) -> None:
        self.queue_name = queue_name
        self.listener = get_listener(
            listener_type, queue_name, connection, self.message_received_callback
        )
        super().__init__(queue_name, sender_type)

    def queue_listener(self) -> None:
        self.listener.consume()

    def message_received_callback(self, message: str) -> None:
        processed_message = self._process_message(message)
        self._post_process_message(processed_message)
        self.save_message(processed_message)

    def _process_message(self, message: str) -> object:
        return json.loads(message)

    def _post_process_message(self, message: object) -> None:
        pass
