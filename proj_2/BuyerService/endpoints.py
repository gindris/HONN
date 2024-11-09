from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from buyer_model import BuyerModel
from container import Container
from buyer_repository import BuyerRepository


router = APIRouter()

@router.get('/buyers/{id}', status_code=200)
@inject
async def get_buyer(id: int, buyer_repository: BuyerRepository = Depends(Provide[Container.buyer_repository_provider])):
    # TODO: get buyer with id
    buyer = await buyer_repository.get_buyer(id)

    if not buyer:
        return {'error': 'buyer not found'}, 404
    return buyer


@router.post('/buyers', status_code=201)
@inject
async def save_buyer(buyer: BuyerModel,
                        buyer_repository: BuyerRepository = Depends(
                            Provide[Container.buyer_repository_provider])):

    # Save the buyer and return the id
    buyer_id = await buyer_repository.save_buyer(buyer)

    return {'id': buyer_id}