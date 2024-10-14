from injector import Module, Binder, provider, singleton

from client.infrastructure.settings.settings import Settings
from client.infrastructure.logging.adapted_logger import AdaptedLogger
from client.repositories.order_repository import OrderRepository
from client.services.payment_service_stub import PaymentServiceStub
from client.infrastructure.logging.i_logger import ILogger
from structured_logging.configuration.logger_config import LoggerConfig

class AppModule(Module):
    def __init__(self, settings: Settings) -> None:
        self.__settings = settings
    
    @provider
    def provide_logger(self) -> AdaptedLogger:
        return AdaptedLogger(LoggerConfig)
    
    @provider
    def provide_payment_service_stub(self, logger: ILogger) -> PaymentServiceStub:
        return PaymentServiceStub(self.__settings, logger)
    
    @provider
    def provide_order_repository(self) -> OrderRepository:
        return OrderRepository(self.__settings)
    
    @provider
    def provide_settings(self) -> Settings:
        return self.__settings

    def configure(self, binder):
        binder.bind(Settings, to=self.__settings)

