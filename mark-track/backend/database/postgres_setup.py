import os
import sys
import logging
import time
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from dotenv import load_dotenv
import psycopg2

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get database credentials
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_NAME = os.getenv("POSTGRES_DB")
DATABASE_HOST = os.getenv("POSTGRES_HOST", "postgres")
DATABASE_PORT = os.getenv("POSTGRES_PORT", "5432")

logger.debug(f"Database configuration: USER={DATABASE_USER}, DB={DATABASE_NAME}")

# Create database URL
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
database = Database(DATABASE_URL)

def wait_for_db(max_retries=30, delay=2):
    """Wait for the database to be ready."""
    retries = 0
    while retries < max_retries:
        try:
            # Try to connect to the database
            conn = psycopg2.connect(
                dbname=DATABASE_NAME,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                port=DATABASE_PORT
            )
            conn.close()
            logger.info("Successfully connected to the database")
            return True
        except psycopg2.OperationalError as e:
            retries += 1
            if retries == max_retries:
                logger.error(f"Could not connect to database after {max_retries} attempts")
                raise e
            logger.warning(f"Database not ready, waiting {delay} seconds... (attempt {retries}/{max_retries})")
            time.sleep(delay)

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


