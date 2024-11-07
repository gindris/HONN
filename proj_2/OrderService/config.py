import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:adminpass@postgres:5433/orders_db')