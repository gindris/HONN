from dependency_injector import containers, providers

from product_repository import ProductRepository


class Container(containers.DeclarativeContainer):

    product_repository_provider = providers.Singleton(
        ProductRepository
    )