from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from models.message_model import MessageModel
from container import Container
from message_repository import MessageRepository
from message_sender import MessageSender

router = APIRouter()


@router.get('/messages/{id}', status_code=200)
@inject
async def get_message(id: int, message_repository: MessageRepository = Depends(Provide[Container.message_repository_provider])):
    # TODO: get message with id
    pass


@router.post('/messages', status_code=201)
@inject
async def save_messages(message: MessageModel,
                        message_sender: MessageSender = Depends(
                            Provide[Container.message_sender_provider]),
                        message_repository: MessageRepository = Depends(
                            Provide[Container.message_repository_provider])):

    # TODO: save message and send message event
    pass
