import pika
from retry import retry


class MessageSender:
    def __init__(self) -> None:
        # TODO: initate connection
        pass

    def send_message(self, message):
        # TODO: send message via rabbitmq
        pass

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        # TODO: create rabbitmq connection
        pass
