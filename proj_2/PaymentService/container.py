from dependency_injector import containers, providers

from payment_repository import PaymentRepository

class Container(containers.DeclarativeContainer):
    payment_service_repository_provider = providers.Singleton(
        PaymentRepository
    )