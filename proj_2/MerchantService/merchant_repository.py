from database import database, metadata, engine
from sqlalchemy import Table, Column, Integer, String, Boolean

merchants_table = Table(
    "merchants",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("ssn", String, nullable=False),
    Column("email", String, nullable=False),
    Column("phoneNumber", String, nullable=False),
    Column("allowsDiscount", Boolean, nullable=False),
)

metadata.create_all(engine)

class MerchantRepository:
    async def save_merchant(self, merchant) -> int:
        # Insert the merchant into the database
        query = merchants_table.insert().values(
            name=merchant.name,
            ssn=merchant.ssn,
            email=merchant.email,
            phoneNumber=merchant.phoneNumber,
            allowsDiscount=merchant.allowsDiscount
        )
        
        merchant_id = await database.execute(query)
        return merchant_id

    def get_merchant(self, id: int) -> str:
        # TODO: return merchant with id from storage
        query = merchants_table.select().where(merchants_table.c.id == id)
        return database.fetch_one(query)