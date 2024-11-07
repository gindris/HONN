from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from models.order_model import OrderModel
from container import Container
from order_repository import OrderRepository
from OrderService.order_events_send import OrderEvents

router = APIRouter()

@router.post("/order")
@inject
async def create_order(order: OrderModel, 
                    order_repository: OrderRepository = 
                        Depends(Provide[Container.order_service_repository_provider]), 
                    order_events: OrderEvents = 
                        Depends(Provide[Container.order_service_events_provider])):
                   
    return await order_repository.create_order(order, order_events)
