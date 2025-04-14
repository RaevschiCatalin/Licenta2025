import sys
import os
import logging
from pathlib import Path
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from models.database_models import Base, Subject
from database.postgres_setup import DATABASE_URL

# Add the backend directory to the Python path
backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from database.postgres_setup import engine, Base
from models.database_models import (
    User, Teacher, Student, Class, ClassStudent,
    Subject, ClassSubject, Mark, Absence, Notification
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_db():
    try:
        # Create engine first
        engine = create_engine(DATABASE_URL)
        
        # Drop all existing tables
        logger.info("Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("All existing tables dropped successfully")
        
        # Create all tables
        logger.info("Creating new tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully")
        
        # Log all created tables
        logger.info("Created tables:")
        for table in Base.metadata.tables:
            logger.info(f" - {table}")
        
        # Populate subjects table
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Check if subjects already exist
        existing_subjects = session.query(Subject).count()
        if existing_subjects == 0:
            # Predefined school subjects
            subjects = [
                "Mathematics",
                "Physics",
                "Chemistry",
                "Biology",
                "History",
                "Geography",
                "English",
                "Romanian",
                "Physical Education",
                "Computer Science",
                "Art",
                "Music"
            ]
            
            # Add subjects to database
            for subject_name in subjects:
                subject = Subject(
                    id=str(uuid.uuid4()),
                    name=subject_name,
                    created_at=datetime.utcnow()
                )
                session.add(subject)
            
            session.commit()
            logger.info("Subjects table populated successfully")
        else:
            logger.info("Subjects table already populated")
            
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    init_db()
    print("Database tables recreated successfully!") 