from abc import ABC, abstractmethod
import json

class ISink(ABC):
    @abstractmethod
    def sink_data(self, data: dict):
        pass



