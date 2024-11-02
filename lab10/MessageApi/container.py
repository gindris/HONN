from dependency_injector import containers, providers

from message_repository import MessageRepository
from message_sender import MessageSender


class Container(containers.DeclarativeContainer):
    message_sender_provider = providers.Singleton(
        MessageSender
    )

    message_repository_provider = providers.Singleton(
        MessageRepository
    )
