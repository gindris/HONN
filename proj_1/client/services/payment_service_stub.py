from injector import inject
from client.infrastructure.logging.i_logger import ILogger
from client.infrastructure.settings.settings import Settings
from client.models.payment import Payment


class PaymentServiceStub():
    @inject
    def __init__(self, settings: Settings, logger: ILogger):
        self.__logger = logger
        self.__settings = settings

    def pay(self, payment: Payment):
        self.__logger.info("Payment started")

        if self.__settings.should_payment_succeed:
            self.__logger.info(f"Payment finished")
        else:
            raise Exception("Payment failed")
