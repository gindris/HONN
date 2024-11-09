from dependency_injector import containers, providers

from order_repository import OrderRepository
from OrderService.order_events_send import OrderEvents

class Container(containers.DeclarativeContainer):
    order_service_repository_provider = providers.Singleton(
        OrderRepository
    )

    order_service_events_provider = providers.Singleton(
        OrderEvents
    )

