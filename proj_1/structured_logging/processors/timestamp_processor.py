from datetime import datetime
from structured_logging.processors.abstract_processor import AbstracProcessor

class TimestampProcessor(AbstracProcessor):
    def process(self, data: dict):
        data['timestamp'] = datetime.now().isoformat()
        return data