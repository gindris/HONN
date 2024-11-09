from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from config import DATABASE_URL

# Create the Database and Engine
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define payments_table
payments_table = Table(
    'payments',
    metadata,
    Column('id', String, primary_key=True),
    Column('orderId', Integer),
    Column('status', String),
)

# Ensure table is created
metadata.create_all(engine)

# Function to save payment result without connecting/disconnecting each time
async def save_payment_result(order_id: int, status: str):
    query = payments_table.insert().values(
        orderId=order_id,
        status=status
    )
    await database.execute(query)
