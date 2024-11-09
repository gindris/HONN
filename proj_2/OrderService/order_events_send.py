import pika
import json
from models.order_model import OrderModel

class OrderEvents:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='rabbitmq',
                heartbeat=600,
                blocked_connection_timeout=300
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='Order-Created', durable=True)

    def send_order_created_event(self, order_data: OrderModel, order_id: int):
        # Convert the order data to a dictionary with just the credit card info
        message = {
            "orderId": order_id,
            "orderData": {
                "cardNumber": order_data.creditCard.cardNumber,
                "expirationMonth": order_data.creditCard.expirationMonth,
                "expirationYear": order_data.creditCard.expirationYear,
                "cvc": order_data.creditCard.cvc
            }
        }
        
        self.channel.basic_publish(
            exchange='',
            routing_key='Order-Created',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                content_type='application/json'
            )
        )
        print(f"Order-Created Event Sent: {json.dumps(message)}")

    def __del__(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()