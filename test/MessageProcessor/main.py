import pika
from retry import retry


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    # TODO: create rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=pika.PlainCredentials('admin', 'lab10')))
    channel = connection.channel()
    channel.queue_declare(queue='messages_queue', durable=True)
    return connection, channel

def callback(ch, method, properties, body):
    entry = body.decode('utf-8')
    print(f"Received message: {entry}")

if __name__ == '__main__':
    # TODO: consume message events and print them to console
    connection = get_connection()[0]
    channel = get_connection()[1]
    channel.basic_consume(queue='messages_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


