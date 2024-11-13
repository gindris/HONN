from database import database, engine, metadata
from sqlalchemy import Table, Column, Integer, String, Float
import requests
from fastapi import HTTPException
from order_events import OrderEvents
from models.order_model import OrderModel

orders_table = Table(
    'orders',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('productId', Integer),
    Column('merchantId', Integer),
    Column('buyerId', Integer),
    Column('cardNumber', String),
    Column('expirationMonth', Integer),
    Column('expirationYear', Integer),
    Column('cvc', Integer),
    Column('discount', Float),
)

metadata.create_all(engine)

class OrderRepository:
    def __init__(self):
        pass

    async def create_order(self, order: OrderModel, order_events: OrderEvents):
        merchant_response = requests.get(f"http://merchant-service:8001/merchants/{order.merchantId}")
        if merchant_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Merchant does not exist")
        if not merchant_response.json()['allowsDiscount'] and order.discount != 0:
            raise HTTPException(status_code=400, detail="Merchant does not allow discount")

        buyer_response = requests.get(f"http://buyer-service:8002/buyers/{order.buyerId}")
        if buyer_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Buyer does not exist")

        product_response = requests.get(f"http://inventory-service:8003/products/{order.productId}")
        if product_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Product does not exist")
        if product_response.json()['quantity'] == 0:
            raise HTTPException(status_code=400, detail="Product is sold out")
        if product_response.json()['merchantId'] != order.merchantId:
            raise HTTPException(status_code=400, detail="Product does not belong to merchant")

        query = orders_table.insert().values(
            productId=order.productId,
            merchantId=order.merchantId,
            buyerId=order.buyerId,
            cardNumber=order.creditCard.cardNumber,
            expirationMonth=order.creditCard.expirationMonth,
            expirationYear=order.creditCard.expirationYear,
            cvc=order.creditCard.cvc,
            discount=order.discount
        )
        order_id = await database.execute(query)
        order_events.send_order_created_event(order, order_id)
        return order_id

    async def get_order(self, order_id: int):
        query = orders_table.select().where(orders_table.c.id == order_id)
        order = await database.fetch_one(query)
        if order is None:
            return None
        
        order = dict(order)
        order['cardNumber'] = '*' * 12 + order['cardNumber'][-4:]
        order = {
            "productId": order['productId'],
            "merchantId": order['merchantId'],
            "buyerId": order['buyerId'],
            "cardNumber": order['cardNumber'],    
            "discount": order['discount']
        }
        return order
        


 