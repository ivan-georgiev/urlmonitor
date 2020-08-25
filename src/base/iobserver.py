"""
Interface to be implemented by classes which to subsribe for notification
"""
from abc import ABC, abstractmethod


class IObserver(ABC):

    @abstractmethod
    def update(self, correlationId: str, msg: object) -> None:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass
