import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:adminpass@localhost:5577/buyer_db')