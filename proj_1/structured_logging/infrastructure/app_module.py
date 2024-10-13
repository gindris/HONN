
from injector import Binder, Module, provider, singleton

from structured_logging.configuration.logger_config import LoggerConfig

class AppModule(Module):
    def __init__(self, logger_config: LoggerConfig) -> None:
        self.__logger_config = logger_config
        
    
#TODO: utfæra þetta almennilega, spurning hvaða providera þarf
    @provider
    @singleton
    def provide_sink(self):
        return self.__logger_config.sink() 
    
    @provider
    @singleton
    def provide_processor(self):
        return self.__logger_config.processor()
    
    @provider
    @singleton
    def provide_is_async(self):
        return self.__logger_config.is_async
    
    @provider
    @singleton
    def provide_async_wait_delay_in_seconds(self):
        return self.__logger_config.async_wait_delay_in_seconds
    
    @provider
    @singleton
    def provide_environment(self):
        return self.__logger_config.environment

    #TODO: nota configure til að binda LoggerConfig við LoggerConfig
    #gera svo providers fyrir föllin í loggerConfig
    def configure(self, binder: Binder) -> None:
        binder.bind(LoggerConfig, to=self.__logger_config)