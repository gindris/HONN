import string
import time
import random
import pika
# TODO: RabbitMQ connection logic goes here
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='logs') 
    return channel

def publish_log(channel, log_entry):
    channel.basic_publish(exchange='', routing_key='logs', body=log_entry)
    print(f'Published log: {log_entry}')

def random_log() -> str:
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))


channel = connect_to_rabbitmq()
while True:
    log_entry = random_log()
    print(f'Publishing log: {log_entry}')
    # TODO: publish logs
    publish_log(channel, log_entry)
    time.sleep(3) 

