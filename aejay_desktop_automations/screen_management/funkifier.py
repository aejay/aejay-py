"""
A module for the funkifier abstractions.
"""
from abc import ABC, abstractmethod
from .funky_state import FunkyState


class Funkifier(ABC):
    """
    The base class for types that can funkify a screen.
    """

    @abstractmethod
    def funkify_screen(self, state: FunkyState):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
