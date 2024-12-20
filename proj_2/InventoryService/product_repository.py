from database import database, metadata, engine
from sqlalchemy import Table, Column, Integer, String, Float

products_table = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("merchantID", Integer, nullable=False),
    Column("productName", String, nullable=False),
    Column("price", Float, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("reserved", Integer, nullable=False)
)

metadata.create_all(engine)

class ProductRepository:
    async def save_product(self, product) -> int:
        # Insert the product into the database
        query = products_table.insert().values(
            merchantID=product.merchantId,
            productName=product.productName,
            price=product.price,
            quantity=product.quantity,
            reserved=0
        )
        
        product_id = await database.execute(query)
        return product_id

    def get_product(self, id: int) -> str:
        # TODO: return product with id from storage
        query = products_table.select().where(products_table.c.id == id)
        return database.fetch_one(query)