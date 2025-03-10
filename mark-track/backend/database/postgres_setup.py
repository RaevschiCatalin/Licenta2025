import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_NAME = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@db/{DATABASE_NAME}"
database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
metadata = MetaData()
Base = sqlalchemy.orm.declarative_base(metadata=metadata)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()


