from dependency_injector.wiring import inject, providers
from fastapi import APIRouter, Depends
from models.order_model import OrderModel
from container import Container
from order_repository import OrderRepository
from order_events import OrderEvents

router = APIRouter()

@router.post("/order")
@inject
async def create_order(order: OrderModel, order_repository: OrderRepository = Depends(Container.order_service_repository_provider)):
    return await order_repository.create_order(order)
