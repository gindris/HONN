import pika
from retry import retry


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    # TODO: create rabbitmq connection
    pass


if __name__ == '__main__':
    # TODO: consume message events and print them to console
    pass
