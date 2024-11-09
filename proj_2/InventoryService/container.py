from dependency_injector import containers, providers

from product_repository import InventoryRepository


class Container(containers.DeclarativeContainer):

    merchant_repository_provider = providers.Singleton(
        InventoryRepository
    )