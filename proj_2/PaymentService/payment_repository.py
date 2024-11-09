import psycopg2
import logging
from config import DATABASE_URL

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaymentRepository:
    def __init__(self):
        # Establish a database connection
        self.db_url = DATABASE_URL  # Ensure this is set to your Postgres URL
        self.connection = psycopg2.connect(self.db_url)
        self.cursor = self.connection.cursor()
        self.initialize_table()
    
    def initialize_table(self):
        # Create table if it does not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment_results (
                order_id TEXT PRIMARY KEY,
                result TEXT
            )
        ''')
        self.connection.commit()
        logger.info("Initialized 'payment_results' table if not present.")

    def save_payment_result(self, order_id: str, result: str):
        try:
            logger.info(f"Saving payment result for order {order_id} with result {result}")
            self.cursor.execute(
                'INSERT INTO payment_results (order_id, result) VALUES (%s, %s) ON CONFLICT (order_id) DO NOTHING',
                (order_id, result)
            )
            self.connection.commit()
            logger.info(f"Payment result for order {order_id} saved successfully.")
        except Exception as e:
            logger.error(f"Error saving payment result for order {order_id}: {e}")
            self.connection.rollback()

    def close(self):
        # Close database connection and cursor
        self.cursor.close()
        self.connection.close()
