import json
from structured_logging.sinks.i_sink import ISink

class ConsoleSink(ISink):
    def sink_data(self, data: dict):
        json_data = json.dumps(data, indent=4) #indent=4 fyrir pretty print.. 
        print(json_data)