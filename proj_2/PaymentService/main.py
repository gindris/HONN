import pika
import json
from retry import retry
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('payment_service')

class PaymentService:
    def __init__(self):
        self.connection = None
        self.channel = None
        logger.info("Initializing Payment Service...")
        self.connect()


    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def connect(self):
        try:
            logger.info("Attempting to connect to RabbitMQ...")
            
            # Connect to RabbitMQ
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            self.channel = self.connection.channel()
            
            # Declare queues
            self.channel.queue_declare(queue='Order-Created', durable=True)
            self.channel.queue_declare(queue='Payment-Succesful', durable=True)
            
            # Set QoS
            self.channel.basic_qos(prefetch_count=1)
            
            logger.info("Successfully connected to RabbitMQ!")
            
            # Check queue status
            queue_info = self.channel.queue_declare(queue='Order-Created', durable=True, passive=True)
            message_count = queue_info.method.message_count
            consumer_count = queue_info.method.consumer_count
            logger.info(f"Order-Created queue status: {message_count} messages, {consumer_count} consumers")
            
            return self.connection, self.channel
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            raise

    def callback(self, ch, method, properties, body):
        try:
            logger.info(f"=== Received new message ===")
            logger.info(f"Raw message: {body}")
            
            # Parse the message
            message = json.loads(body.decode('utf-8'))
            logger.info(f"Processed message content: {json.dumps(message, indent=2)}")
            
            # Extract order details
            order_id = message['orderId']
            card_info = message['orderData']
            logger.info(f"Processing payment for order ID: {order_id}")
            logger.info(f"Card info (last 4 digits): ...{card_info['cardNumber'][-4:]}")
            
            # Process payment (validate card, etc.)
            payment_status = "Success"  # Your validation logic here
            logger.info(f"Payment status: {payment_status}")
            
            # Send payment processed event
            response = {
                "orderId": order_id,
                "status": payment_status
            }
            self.channel.basic_publish(
                exchange='',
                routing_key='Payment-Succesful',
                body=json.dumps(response),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            logger.info(f"Published payment result: {response}")
            
            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info("Message processing completed successfully")
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def start_consuming(self):
        try:
            logger.info("Starting payment service consumer...")
            
            self.channel.basic_consume(
                queue='Order-Created',
                on_message_callback=self.callback,
                auto_ack=False
            )
            
            logger.info(" [*] Payment Service waiting for messages. To exit press CTRL+C")
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("Shutting down payment service...")
            if self.connection and not self.connection.is_closed:
                self.connection.close()
        except Exception as e:
            logger.error(f"Unexpected error in payment service: {str(e)}", exc_info=True)
            if self.connection and not self.connection.is_closed:
                self.connection.close()

if __name__ == '__main__':
    try:
        logger.info("Starting Payment Service...")
        service = PaymentService()
        service.start_consuming()
    except Exception as e:
        logger.error(f"Failed to start Payment Service: {str(e)}", exc_info=True)
        sys.exit(1)