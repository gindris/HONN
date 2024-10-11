import json
from structured_logging.sinks.i_sink import ISink

class FileSink(ISink):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def sink_data(self, data: dict):
        json_data = json.dumps(data, indent=4)
        with open(self.file_path, 'a') as file:
            file.write(json_data + '\n')