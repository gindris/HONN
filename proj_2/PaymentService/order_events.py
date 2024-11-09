import pika
import json

class OrderEvents:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='Order-Created', durable=True)
        self.channel.queue_declare(queue='payment_service_messages_queue', durable=True)

    def validate_payment(self, credit_card):
        # Simplified validation logic here
        return credit_card['cvc'] == 123

    def send_payment_event(self, order_id, success):
        status = "success" if success else "failure"
        payment_event = {
            "orderId": order_id,
            "status": status
        }
        message = json.dumps(payment_event)
        self.channel.basic_publish(
            exchange='',
            routing_key='payment_service_messages_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2 #gerir message persistent
            )
        )
        print(f"Payment-{status.capitalize()} Event Sent: {message}")

    def on_order_created(self, ch, method, properties, body):
        print(f"Received Order-Created Event: {body}")
        data = json.loads(body)
        
        # Validate payment
        success = self.validate_payment(data["orderData"])
        
        # Send payment event based on validation
        self.send_payment_event(data['orderId'], success)
        
        # Acknowledge message consumption
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_consume(queue='Order-Created', on_message_callback=self.on_order_created)
        print("Waiting for Order-Created events...")
        self.channel.start_consuming()
