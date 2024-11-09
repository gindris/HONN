from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from product_model import ProductModel
from container import Container
from product_repository import ProductRepository


router = APIRouter()

@router.get('/products/{id}', status_code=200)
@inject
async def get_product(id: int, product_repository: ProductRepository = Depends(Provide[Container.product_repository_provider])):
    # TODO: get product with id
    product = await product_repository.get_product(id)

    if not product:
        return {'error': 'product not found'}, 404
    return product


@router.post('/products', status_code=201)
@inject
async def save_product(product: ProductModel,
                        product_repository: ProductRepository = Depends(
                            Provide[Container.product_repository_provider])):

    # Save the product and return the id
    product_id = await product_repository.save_product(product)

    return {'id': product_id}

@router.patch('/products/{id}/reserve', status_code=200)
@inject
async def reserve_product(id: int, quantity: int,
                          product_repository: ProductRepository = Depends(
                              Provide[Container.product_repository_provider])):
    product = await product_repository.get_product(id)
    if not product:
        return {'error': 'product not found'}, 404
    
    if product['quantity'] < quantity:
        return {'error': 'not enough quantity'}, 400
    
    # Reserve quantity of product with id
    success = await product_repository.reserve_product(id, quantity)
