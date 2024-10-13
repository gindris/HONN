

#klasi sem erfir frá command og executar log skipun
#queue á að taka inn þetta LoggerCommand og execute-a það


from logging import Logger
from typing import Any, Iterable

from proj_1.structured_logging.command_queue.command import Command


class LoggerCommand (Command):
    def __init__(self, logger: Logger, **kwargs: Iterable[Any]):
        self.__logger = logger
        self.__kwargs = kwargs
        self.async_delay = logger.logger_config.async_delay #exposa async_delay úr loggerConfig svo queue geti notað það

    def execute(self):
        self.__logger.sink_data(self.__kwargs) 
    #bjó til fall sink_data í logger sem keyrir viðeigandi sink_data úr loggerConfig