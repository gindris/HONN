import pika
import json
from OrderService.models.order_model import OrderModel

class OrderEvents:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='Order-Created', durable=True)

    def send_order_created_event(self, order_data: OrderModel, order_id: int):
        message = json.dumps({
            "orderId": order_id,
            "orderData": order_data.creditCard
        })
        self.channel.basic_publish(
            exchange='', 
            routing_key='Order-Created', 
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2 
            )
        )
        print(f"Order-Created Event Sent: {message}")