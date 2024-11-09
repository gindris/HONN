from database import database, metadata, engine
from sqlalchemy import Table, Column, Integer, String

buyers_table = Table(
    "buyers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("ssn", String, nullable=False),
    Column("email", String, nullable=False),
    Column("phoneNumber", String, nullable=False)
)

metadata.create_all(engine)

class BuyerRepository:
    async def save_buyer(self, buyer) -> int:
        # Insert the buyer into the database
        query = buyers_table.insert().values(
            name=buyer.name,
            ssn=buyer.ssn,
            email=buyer.email,
            phoneNumber=buyer.phoneNumber
        )
        
        buyer_id = await database.execute(query)
        return buyer_id

    def get_buyer(self, id: int) -> str:
        # TODO: return buyer with id from storage
        query = buyers_table.select().where(buyers_table.c.id == id)
        return database.fetch_one(query)