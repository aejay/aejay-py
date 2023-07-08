from abc import ABC, abstractmethod
from .FunkyState import FunkyState

class Funkifier(ABC):
    
    @abstractmethod
    def funkify_screen(self, state: FunkyState):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
    