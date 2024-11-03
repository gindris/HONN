from database import database, metadata, engine
from sqlalchemy import Table, Column, Integer, String

messages_table = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("content", String, nullable=False)
)

metadata.create_all(engine)

class MessageRepository:
    async def save_message(self, message) -> int:
        # TODO: save message to persistent storage and return id
        query = messages_table.insert().values(content=message)
        message_id = await database.execute(query)
        return message_id

    def get_message(self, id: int) -> str:
        # TODO: return message with id from storage
        query = messages_table.select().where(messages_table.c.id == id)
        return database.fetch_one(query)
