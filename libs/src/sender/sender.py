from abc import ABC, abstractmethod
from typing import Any, Self


class Sender(ABC):
    @classmethod
    @abstractmethod
    def create_connection(self, connection: Any | None) -> Self:
        pass

    @abstractmethod
    def send_message(self, message: object) -> None:
        pass

    @abstractmethod
    def _check_connection(self) -> bool:
        pass
