import pika
import json
from retry import retry
import sys
import logging
from container import Container

# logging til að debugga rabbitmq... 
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
        self.container = Container()
        self.payment_repository = self.container.payment_service_repository_provider()


    def validate_creditcard(self, card_info: dict) -> bool:
        try:
            def luhn_check(number: str) -> bool:
                number = number.replace(" ", "").replace("-", "")
                if not number.isdigit():
                    return False
                digits = [int(d) for d in number][::-1]
                for i in range(1, len(digits), 2):
                    digits[i] *= 2
                    if digits[i] > 9:
                        digits[i] -= 9
                return sum(digits) % 10 == 0
            
            if not all([card_info['cardNumber'], card_info['expirationMonth'], card_info['expirationYear'], card_info['cvc']]):
                return False
            
            if not luhn_check(card_info['cardNumber']):
                return False
            
            if not 1 <= int(card_info['expirationMonth']) <= 12:
                return False
            #
            if len(str(card_info['expirationYear'])) != 4:
                return False
            
            if len(str(card_info['cvc'])) != 3:
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating credit card: {str(e)}")
            return False
        

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def connect(self):
        try:
            logger.info("Attempting to connect to RabbitMQ...")
            
            # RabbitMQ tenging
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            self.channel = self.connection.channel()
            
            self.channel.queue_declare(queue='Order-Created', durable=True)
            self.channel.queue_declare(queue='Payment-Succesful', durable=True)
            
            self.channel.basic_qos(prefetch_count=1)
            
            logger.info("Successfully connected to RabbitMQ!")
            
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
            
            message = json.loads(body.decode('utf-8'))
            logger.info(f"Processed message content: {json.dumps(message, indent=2)}")
            
            order_id = message['orderId']
            card_info = message['orderData']
    
            if self.validate_creditcard(card_info):
                payment_status = "Success"
                #send a 'Payment-Successful' event
                self.channel.basic_publish(
                    exchange='',
                    routing_key='Payment-Succesful',
                    body=json.dumps(message),
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        content_type='application/json'
                    )
                )
            else:
                payment_status = "Failed"
                #send a 'Payment-Failed' event
                self.channel.basic_publish(
                    exchange='',
                    routing_key='Payment-Failed',
                    body=json.dumps(message),
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        content_type='application/json'
                    )
                )

            logger.info(f"Payment status: {payment_status}")
            
            response = {
                "orderId": order_id,
                "status": payment_status
            }
            
            self.payment_repository.save_payment_result(order_id, payment_status)

            logger.info(f"Published payment result: {response}")
            
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