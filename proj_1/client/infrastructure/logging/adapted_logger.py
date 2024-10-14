from injector import inject
from client.infrastructure.logging.i_logger import ILogger
from structured_logging.configuration.logger_config import LoggerConfig
from structured_logging.logger.logger import Logger

class AdaptedLogger(ILogger):
    @inject
    def __init__(self, logger_config: LoggerConfig): #Taka inn structured logger og aðlaga að ILogger interface
        self._logger = Logger(logger_config)

    #formatta logga eftir type til að implementa ILogger interface og logga með structured logger
    def error(self, message: str, exception: Exception = None):
        log_data = {
            'message': message,
            'exception': str(exception)
        }
        self._logger.log(log_data)

    def warning(self, message: str, exception: Exception = None):
        log_data = {
            'message': message,
            'exception': str(exception)
        }
        self._logger.log(log_data)

    def info(self, message: str):
        log_data = {
            'message': message
        }
        self._logger.log(log_data)
        