import pika
# TODO: You need to implement the consumption logic and connection to RabbitMQ here.
def callback(ch, method, properties, body):
    log_entry = body.decode('utf-8') 
    print(f'Consumed log: {log_entry}')
    log_to_file(log_entry) 


def log_to_file(log_entry: str):
    with open('./log.log', 'a+') as log_file:
        log_file.write(log_entry + '\n')
        log_file.flush()

print('Waiting for logs....')
# TODO: consume logs here
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='logs') 
channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)

print('Waiting for logs...')
channel.start_consuming()


