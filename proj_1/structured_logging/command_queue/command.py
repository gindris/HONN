from abc import ABC, abstractmethod

#abstract klasi, ekki snerta
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
