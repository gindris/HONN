from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from merchant_model import MerchantModel
from container import Container
from merchant_repository import MerchantRepository


router = APIRouter()

@router.get('/merchants/{id}', status_code=200)
@inject
async def get_merchant(id: int, merchant_repository: MerchantRepository = Depends(Provide[Container.merchant_repository_provider])):
    # TODO: get merchant with id
    merchant = await merchant_repository.get_merchant(id)

    if not merchant:
        return {'error': 'merchant not found'}, 404
    return merchant


@router.post('/merchants', status_code=201)
@inject
async def save_merchant(merchant: MerchantModel,
                        merchant_repository: MerchantRepository = Depends(
                            Provide[Container.merchant_repository_provider])):

    # Save the merchant and return the id
    merchant_id = await merchant_repository.save_merchant(merchant)

    return {'id': merchant_id}