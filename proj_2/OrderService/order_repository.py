from database import database, engine, metadata
from sqlalchemy import Table, Column, Integer, String, Float
import requests

from models.order_model import OrderModel
orders_table = Table(
    'orders',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('productId', Integer),
    Column('merchantId', Integer),
    Column('buyerId', Integer),
    Column('cardNumber', String),
    Column('totalPrice', Float)
)

class OrderRepository:
    async def create_order(self, order: OrderModel):
        #        OrderService ætti að skila 400 HTTP Status Code með villuskilaboðunum "Merchant does not
        # exist" ef það er ekki til seljandi með tiltekið merchantId.
        #fetching from localhost:8001/merchant/{order.merchantId}
        merchant_response = await requests.get(f"http://localhost:8001/merchant/{order.merchantId}")

        # •OrderService ætti að skila 400 HTTP Status Code með villuskilaboðunum "Buyer does not
        # exist" ef það er ekki til kaupandi með tiltekið buyerId
        buyer_response = await requests.get(f"http://localhost:8002/buyer/{order.buyerId}")
        
        # •OrderService ætti að skila 400 HTTP Status Code með villuskilaboðunum "Product does not
        # exist" Ef vara er ekki til með tilekið productId
        product_response = await requests.get(f"http://localhost:8003/product/{order.productId}")

        # •OrderService ætti að skila 400 HTTP Status Code með villuskilaboðunum "Product is sold out"
        # Ef vara með tiltekið productId er uppseld
        product_stock_response = await requests.get(f"http://localhost:8003/product/{order.productId}")
        #ef uppseld

        # •OrderService ætti að skila 400 HTTP Status Code með villuskilaboðunum "Product does not
        # belong to merchant" ef seljandi með merchantId á ekki vöru með productId.
        product_merchant_response = await requests.get(f"http://localhost:8003/product/{order.productId}")
        if product_merchant_response.json()['merchantId'] != order.merchantId:
            return 400, "Product does not belong to merchant"
        
        # •OrderService ætti að skila 400 HTTP Status Code með villuskilaboðunum "Merchant does
        # not allow discount" ef seljandi með merchantId leyfir ekki afslátt og tilgreindur discount er
        # eitthvað annað en null eða 0.
        
        # •Ef allt validation gengur upp þá ætti OrderService að taka frá vöruna, vista kaup-in í gagna-
        # grunn, senda event um að kaup hafa verið stofnuð og skila 201 HTTP Status Code með order
        # id-i sem response message.

 