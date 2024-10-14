import json

from structured_logging.sinks.console_sink import ConsoleSink

def test_console_sink(capfd):
    sink = ConsoleSink()
    log_data = {
        "level": "INFO",
        "message": "Test message",
        "timestamp": "2024-10-07T14:00:00"
    }

    sink.sink_data(log_data)

    # Capture the printed output
    captured = capfd.readouterr()

    #checkum ef ef captured output er eins og expected, 'i ConsoleSink er json.dumps... 
    #kóðalínan sem prentar út gögnin með indent=4
    expected_output = json.dumps(log_data, indent=4) + "\n"
    assert captured.out == expected_output

from structured_logging.sinks.file_sink import FileSink
import os

def test_file_sink(tmp_path):
    file_path = os.path.join(tmp_path, "test.log")
    sink = FileSink(file_path)
    log_data = {
        "level": "INFO",
        "message": "Test message",
        "timestamp": "2024-10-07T14:00:00"
    }

    sink.sink_data(log_data)

    with open(file_path, 'r') as file:
        content = file.read() 

    expected_output = json.dumps(log_data, indent=4) + "\n"
    assert content == expected_output

