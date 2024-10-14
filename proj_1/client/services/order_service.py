from injector import inject
from client.models.order import Order
from client.repositories.order_repository import OrderRepository
from client.services.payment_service_stub import PaymentServiceStub
from client.infrastructure.logging.i_logger import ILogger


class OrderService:
    @inject
    def __init__(self, payment_service: PaymentServiceStub, order_repository: OrderRepository, logger: ILogger):
        self.__payment_service = payment_service
        self.__logger = logger
        self.__order_repository = order_repository

    def place_order(self, order: Order):
        self.__logger.info("Order started")

        self.__payment_service.pay(order.payment)
        self.__order_repository.save(order)

        self.__logger.info("Order finished")
