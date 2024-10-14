from typing import Any, Iterable

from injector import inject
from structured_logging.logger.loggerCommand import LoggerCommand
from structured_logging.command_queue.queue import Queue
from structured_logging.configuration.logger_config import LoggerConfig
from structured_logging.command_queue.command import Command


class Logger:
    @inject
    def __init__(self, logger_config: LoggerConfig, logging_queue: Queue):
        self.__logger_config = logger_config
        self.__logging_queue = logging_queue

    def log(self, **kwargs: Iterable[Any]):
        processor = self.__logger_config.processor #TODO: þarf að laga
        data = processor.handle(kwargs)

        command = LoggerCommand(self.__logger_config.sink, data)
        if self.__logger_config.is_async:
            self.__logging_queue.add(command)
        else: 
            command.execute()
