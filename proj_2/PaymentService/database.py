from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from config import DATABASE_URL

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()
