import pika
from retry import retry


class MessageSender:
    def __init__(self) -> None:
        # TODO: initate connection
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='messages_queue', durable=True)

    def send_message(self, message):
        # TODO: send message via rabbitmq
        self.channel.basic_publish(exchange='', routing_key='messages_queue', body=message)
        print(f"Message sent: {message}")

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        # TODO: create rabbitmq connection
        return pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=pika.PlainCredentials('admin', 'lab10')))
