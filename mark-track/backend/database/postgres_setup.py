import os
import sys
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get database credentials
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_NAME = os.getenv("POSTGRES_DB")

logger.debug(f"Database configuration: USER={DATABASE_USER}, DB={DATABASE_NAME}")

# Create database URL
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@postgres/{DATABASE_NAME}"
database = Database(DATABASE_URL)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData()

# Create declarative base
Base = declarative_base()

# Create session factory
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


