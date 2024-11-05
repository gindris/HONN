import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:lab10@postgres:5432/lab10_messages')