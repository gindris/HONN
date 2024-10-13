from injector import Module, Binder, provider, singleton

from client.infrastructure.settings.settings import Settings

class AppModule(Module):
    def __init__(self, settings: Settings) -> None:
        self.__settings = settings
    
    @singleton
    @provider
    def provide_order_file_path(self) -> str:
        return self.__settings.order_file_path
    
    @singleton
    @provider
    def provide_should_payment_succeed(self) -> bool:
        return self.__settings.should_payment_succeed
    
    @singleton
    @provider
    def provide_logging_type(self) -> str:
        return self.__settings.logging_type
    
    @singleton
    @provider
    def provide_logging_file_path(self) -> str:
        return self.__settings.logging_file_path
    
    @singleton
    @provider
    def provide_logging_is_async(self) -> bool:
        return self.__settings.logging_is_async
    
    @singleton
    @provider
    def provide_logging_async_delay(self) -> int:
        return self.__settings.logging_async_delay
    
    @singleton
    @provider
    def provide_environment(self) -> str:
        return self.__settings.environment

    def configure(self, binder):
        binder.bind(Settings, to=self.__settings)

