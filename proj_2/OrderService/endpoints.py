from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from models.order_model import OrderModel
from container import Container
from order_repository import OrderRepository
from order_events import OrderEvents

router = APIRouter()

@router.post("/orders", status_code=201)
@inject
async def create_order(order: OrderModel, 
                    order_repository: OrderRepository = 
                        Depends(Provide[Container.order_service_repository_provider]), 
                    order_events: OrderEvents = 
                        Depends(Provide[Container.order_service_events_provider])):
                   
    order_id = await order_repository.create_order(order, order_events)
    return {"orderId": order_id}

@router.get("/orders/{order_id}")
@inject
async def get_order(order_id: int, 
                    order_repository: OrderRepository = 
                        Depends(Provide[Container.order_service_repository_provider])):
    order = await order_repository.get_order(order_id)
    if order is None:
        return 404, "Order does not exist"
    return order