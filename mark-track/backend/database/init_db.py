import sys
import os
import logging
from pathlib import Path
import uuid
from datetime import datetime
from sqlalchemy import create_engine, inspect
from models.database_models import Base, Subject
from database.postgres_setup import DATABASE_URL
from sqlalchemy.sql import text

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

def create_sample_users(session):
    # Create sample users with different roles
    users = [
        # Teacher users
        User(
            id=str(uuid.uuid4()),
            email="john.doe@school.com",
            password="teacher123",
            role="teacher",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="jane.smith@school.com",
            password="teacher123",
            role="teacher",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="michael.brown@school.com",
            password="teacher123",
            role="teacher",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="sarah.wilson@school.com",
            password="teacher123",
            role="teacher",
            created_at=datetime.utcnow()
        ),
        # Student users
        User(
            id=str(uuid.uuid4()),
            email="alice.johnson@school.com",
            password="student123",
            role="student",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="bob.williams@school.com",
            password="student123",
            role="student",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="emma.davis@school.com",
            password="student123",
            role="student",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="james.miller@school.com",
            password="student123",
            role="student",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="olivia.taylor@school.com",
            password="student123",
            role="student",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="william.anderson@school.com",
            password="student123",
            role="student",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="sophia.thomas@school.com",
            password="student123",
            role="student",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="ethan.jackson@school.com",
            password="student123",
            role="student",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="isabella.white@school.com",
            password="student123",
            role="student",
            created_at=datetime.utcnow()
        ),
        User(
            id=str(uuid.uuid4()),
            email="mason.harris@school.com",
            password="student123",
            role="student",
            created_at=datetime.utcnow()
        ),
    ]
    
    for user in users:
        session.add(user)
    session.commit()
    return users

def create_sample_teachers(session, users):
    # Create sample teachers
    teachers = [
        Teacher(
            id=str(uuid.uuid4()),
            first_name="John",
            last_name="Doe",
            father_name="Michael",
            gov_number="T12345",
            subject_id=session.query(Subject).filter_by(name="Mathematics").first().id,
            user_id=users[0].id
        ),
        Teacher(
            id=str(uuid.uuid4()),
            first_name="Jane",
            last_name="Smith",
            father_name="Robert",
            gov_number="T67890",
            subject_id=session.query(Subject).filter_by(name="Physics").first().id,
            user_id=users[1].id
        ),
        Teacher(
            id=str(uuid.uuid4()),
            first_name="Michael",
            last_name="Brown",
            father_name="David",
            gov_number="T24680",
            subject_id=session.query(Subject).filter_by(name="Chemistry").first().id,
            user_id=users[2].id
        ),
        Teacher(
            id=str(uuid.uuid4()),
            first_name="Sarah",
            last_name="Wilson",
            father_name="James",
            gov_number="T13579",
            subject_id=session.query(Subject).filter_by(name="Biology").first().id,
            user_id=users[3].id
        ),
    ]
    
    for teacher in teachers:
        session.add(teacher)
    session.commit()
    return teachers

def create_sample_students(session, users):
    # Create sample students
    students = [
        Student(
            id=str(uuid.uuid4()),
            student_id="LTMV2221",
            first_name="Alice",
            last_name="Johnson",
            father_name="David",
            gov_number="S12345",
            user_id=users[4].id
        ),
        Student(
            id=str(uuid.uuid4()),
            student_id="LTMV2222",
            first_name="Bob",
            last_name="Williams",
            father_name="James",
            gov_number="S67890",
            user_id=users[5].id
        ),
        Student(
            id=str(uuid.uuid4()),
            student_id="LTMV2223",
            first_name="Emma",
            last_name="Davis",
            father_name="Robert",
            gov_number="S24680",
            user_id=users[6].id
        ),
        Student(
            id=str(uuid.uuid4()),
            student_id="LTMV2224",
            first_name="James",
            last_name="Miller",
            father_name="William",
            gov_number="S13579",
            user_id=users[7].id
        ),
        Student(
            id=str(uuid.uuid4()),
            student_id="LTMV2225",
            first_name="Olivia",
            last_name="Taylor",
            father_name="Thomas",
            gov_number="S97531",
            user_id=users[8].id
        ),
        Student(
            id=str(uuid.uuid4()),
            student_id="LTMV2226",
            first_name="William",
            last_name="Anderson",
            father_name="George",
            gov_number="S86420",
            user_id=users[9].id
        ),
        Student(
            id=str(uuid.uuid4()),
            student_id="LTMV2227",
            first_name="Sophia",
            last_name="Thomas",
            father_name="Edward",
            gov_number="S75319",
            user_id=users[10].id
        ),
        Student(
            id=str(uuid.uuid4()),
            student_id="LTMV2228",
            first_name="Ethan",
            last_name="Jackson",
            father_name="Henry",
            gov_number="S64208",
            user_id=users[11].id
        ),
        Student(
            id=str(uuid.uuid4()),
            student_id="LTMV2229",
            first_name="Isabella",
            last_name="White",
            father_name="Charles",
            gov_number="S53197",
            user_id=users[12].id
        ),
        Student(
            id=str(uuid.uuid4()),
            student_id="LTMV2230",
            first_name="Mason",
            last_name="Harris",
            father_name="Daniel",
            gov_number="S42086",
            user_id=users[13].id
        ),
    ]
    
    for student in students:
        session.add(student)
    session.commit()
    return students

def create_sample_classes(session):
    # Create sample classes
    classes = [
        Class(
            id="4B",
            name="4B",
            created_at=datetime.utcnow()
        ),
        Class(
            id="5C",
            name="5C",
            created_at=datetime.utcnow()
        ),
        Class(
            id="6A",
            name="6A",
            created_at=datetime.utcnow()
        ),
    ]
    
    for class_ in classes:
        session.add(class_)
    session.commit()
    return classes

def init_db():
    try:
        # Create engine first
        engine = create_engine(DATABASE_URL)
      
        # Create all tables based on models if they don't exist
        logger.info("Creating tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        
        # Log all tables
        logger.info("Existing tables:")
        inspector = inspect(engine)
        for table in inspector.get_table_names():
            logger.info(f" - {table}")
        
        # Create session
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            # Check if we already have data
            existing_subjects = session.query(Subject).first()
            if existing_subjects:
                logger.info("Database already contains data, skipping initialization")
                return

            # Step 1: Create and insert subjects first (needed for teachers)
            subjects = [
                "Mathematics", "Physics", "Chemistry", "Biology",
                "History", "Geography", "English", "Romanian",
                "Physical Education", "Computer Science", "Art", "Music"
            ]
            
            for subject_name in subjects:
                subject = Subject(
                    id=str(uuid.uuid4()),
                    name=subject_name,
                    created_at=datetime.utcnow()
                )
                session.add(subject)
            session.commit()
            logger.info("Subjects created successfully")

            # Step 2: Create and insert users (needed for teachers and students)
            users = create_sample_users(session)
            session.commit()
            logger.info("Users created successfully")

            # Step 3: Create and insert teachers
            teachers = create_sample_teachers(session, users)
            session.commit()
            logger.info("Teachers created successfully")

            # Step 4: Create and insert students
            students = create_sample_students(session, users)
            session.commit()
            logger.info("Students created successfully")

            # Step 5: Create and insert classes
            classes = create_sample_classes(session)
            session.commit()
            logger.info("Classes created successfully")

            # Step 6: Create class-student relationships
            # Get fresh list of students and classes from database
            db_students = session.query(Student).all()
            db_classes = session.query(Class).all()

            if not db_students:
                raise Exception("No students found in database")
            if not db_classes:
                raise Exception("No classes found in database")

            # Create class-student relationships
            for i, student in enumerate(db_students):
                class_id = db_classes[i % len(db_classes)].id
                session.execute(text("""
                    INSERT INTO class_students (class_id, student_id)
                    VALUES (:class_id, :student_id)
                """), {
                    'class_id': class_id,
                    'student_id': student.student_id
                })
            session.commit()
            logger.info("Class-student relationships created successfully")

            # Step 7: Create class-subject-teacher relationships
            db_subjects = session.query(Subject).all()
            db_teachers = session.query(Teacher).all()

            for class_ in db_classes:
                for i, teacher in enumerate(db_teachers):
                    if i < len(db_subjects):
                        session.execute(text("""
                            INSERT INTO class_subjects (class_id, subject_id, teacher_id)
                            VALUES (:class_id, :subject_id, :teacher_id)
                        """), {
                            'class_id': class_.id,
                            'subject_id': db_subjects[i].id,
                            'teacher_id': teacher.id
                        })
            session.commit()
            logger.info("Class-subject-teacher relationships created successfully")
            
        except Exception as e:
            session.rollback()
            raise e
            
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    init_db()
    print("Database initialization completed successfully!") 