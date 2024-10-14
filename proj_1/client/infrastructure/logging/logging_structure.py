from infrastructure.logging.i_logger import ILogger

class LoggerStructure(ILogger):
    def __init__(self, logger: ILogger):
        self._logger = logger

    def error(self, message: str, exception: Exception = None):
        log_data = {
            'message': message,
            'exception': str(exception)
        }
        self._logger.error(log_data)

    def warning(self, message: str, exception: Exception = None):
        log_data = {
            'message': message,
            'exception': str(exception)
        }
        self._logger.warning(log_data)

    def info(self, message: str):
        log_data = {
            'message': message
        }
        self._logger.info(log_data)
        