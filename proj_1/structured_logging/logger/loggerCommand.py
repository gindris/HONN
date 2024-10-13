

#klasi sem erfir frá command og executar log skipun
#queue á að taka inn þetta LoggerCommand og execute-a það


from logging import Logger
from typing import Any, Iterable

from structured_logging.sinks.i_sink import ISink
from structured_logging.command_queue.command import Command


class LoggerCommand (Command):
    def __init__(self, sink: ISink, data: dict):
        self.__sink = sink
        self.__data = data 
    
    def execute(self):
        self.__sink.sink_data(self.__data)
        return self.__data
        