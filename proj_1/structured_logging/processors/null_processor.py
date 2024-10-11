from .abstract_processor import AbstracProcessor

class NullProcessor(AbstracProcessor):
    def process(self, data: dict):
        return data