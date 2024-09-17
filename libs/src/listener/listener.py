from abc import ABC, abstractmethod
from typing import Any


class Listener(ABC):
    @abstractmethod
    def consume(self) -> None:
        pass

    @abstractmethod
    def _callback(self, ch: Any, method: Any, properties: Any, body: Any) -> None:
        pass
