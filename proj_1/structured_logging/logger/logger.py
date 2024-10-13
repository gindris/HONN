from typing import Any, Iterable
from proj_1.structured_logging.logger.loggerCommand import LoggerCommand
from structured_logging.command_queue.queue import Queue
from structured_logging.configuration.logger_config import LoggerConfig
from structured_logging.command_queue.command import Command


class Logger:
    def __init__(self, logger_config: LoggerConfig, logging_queue: Queue):
        self.__logger_config = logger_config
        self.__logging_queue = logging_queue

    def sink_data(self, data: dict):
        self.__logger_config.sink_data(data)

    def log(self, **kwargs: Iterable[Any]):
        self.__logger_config
        #TODO:
        #1. Höndla processors spurning hvort valid ???
        processors = self.__logger_config.processors
        for processor in processors:
            processor.process(kwargs)
        #2. Búa til logging command
        #TODO: finna út hvernig logging command getur notað sink data aðferðina
        log_commmand = LoggerCommand(self, **kwargs)
        #3. setja í queue ef async
        if self.__logger_config.is_async:
            self.__logging_queue.add(log_commmand)
        #   annars keyra strax
        else:
            log_commmand.execute()