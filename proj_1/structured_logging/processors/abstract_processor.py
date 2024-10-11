from abc import ABC, abstractmethod
from datetime import datetime
from structured_logging.processors.i_processor import IProcessor

class AbstracProcessor(IProcessor):
    def __init__(self):
        self._next_processor: IProcessor = None

    def set_next(self, processor: IProcessor):
        self._next_processor = processor
        return processor

    def handle(self, data: dict):
        data = self.process(data)

        if self._next_processor:
            return self._next_processor.handle(data)
        return None
    
    @abstractmethod
    def process(self, data: dict):
        pass