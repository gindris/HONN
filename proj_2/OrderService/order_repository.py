from database import database, engine, metadata
from sqlalchemy import Table, Column, Integer, String, Float
import requests
from OrderService.order_events import OrderEvents

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
    Column('cvv', Integer),
    Column('discount', Float)
)

class OrderRepository:
    async def create_order(self, order: OrderModel):
        merchant_response = await requests.get(f"http://localhost:8001/merchant/{order.merchantId}")
        if merchant_response.status_code == 404:
            return 400, "Merchant does not exist"
    
        buyer_response = await requests.get(f"http://localhost:8002/buyer/{order.buyerId}")
        if buyer_response.status_code == 404:
            return 400, "Buyer does not exist"
            
        product_response = await requests.get(f"http://localhost:8003/product/{order.productId}")
        if product_response.status_code == 404:
            return 400, "Product does not exist"

        product_quantity_response = await requests.get(f"http://localhost:8003/product/{order.productId}")
        if product_quantity_response.json()['quantity'] == 0:
            return 400, "Product is sold out"
       
        product_merchant_response = await requests.get(f"http://localhost:8003/product/{order.productId}")
        if product_merchant_response.json()['merchantId'] != order.merchantId:
            return 400, "Product does not belong to merchant"
        
        merchant_discount_response = await requests.get(f"http://localhost:8001/merchant/{order.merchantId}")
        if merchant_discount_response.json()['allowsDiscount'] == False and order.discount != 0:
            return 400, "Merchant does not allow discount"
        
        # •Ef allt validation gengur upp þá ætti OrderService að taka frá vöruna, vista kaup-in í gagna-
        # grunn, senda event um að kaup hafa verið stofnuð og skila 201 HTTP Status Code með order
        # id-i sem response message.
        order_sender = OrderEvents()
        order_sender.send_message(order.creditCard)
        response = await order_sender.consume_message_payment_service
        if response == False:
            return 400, "Payment failed, credit card is invalid"
        
        query = orders_table.insert().values(
            productId=order.productId,
            merchantId=order.merchantId,
            buyerId=order.buyerId,
            cardNumber=order.creditCard.cardNumber,
            expirationMonth=order.creditCard.expirationMonth,
            expirationYear=order.creditCard.expirationYear,
            cvv=order.creditCard.cvv,
            discount=order.discount
        )
        order_id = await database.execute(query)
        


 