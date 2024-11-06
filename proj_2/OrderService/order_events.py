import pika
from retry import retry

class OrderEvents:
    def __init__(self) -> None:
        self.connection_order_service = self.__get_connection_order_service()
        self.channel_order_service = self.connection_order_service.channel()
        self.channel_order_service.queue_declare(queue='order_service_messages_queue', durable=True)

        self.connection_payment_service, self.channel_payment_service = self.get_connection_payment_service()

    def send_message(self, message):
        self.channel_order_service.basic_publish(exchange='', routing_key='order_service_messages_queue', body=message)
        print(f"Message sent: {message}")

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection_order_service(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host='orderService', credentials=pika.PlainCredentials('orderadmin', 'orderservice')))

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def get_connection_payment_service(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='paymentService', credentials=pika.PlainCredentials('paymentadmin', 'paymentservice')))
        channel = connection.channel()
        channel.queue_declare(queue='payment_service_messages_queue', durable=True)
        return connection, channel
    
    def callback(self, ch, method, properties, body):
        """held þetta geti verið universal callback fall ?"""
        print(f"Received {body}")
    
    def consume_message_payment_service(self):
        self.channel_payment_service.basic_consume(queue='payment_service_messages_queue', on_message_callback=self.callback, auto_ack=True)
        response = self.channel_payment_service.start_consuming()
        return response