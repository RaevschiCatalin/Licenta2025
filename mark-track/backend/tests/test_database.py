import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import time
from models.database_models import User, Teacher
from database.postgres_setup import engine, Base

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_database_connection_pool(db_session):
    start_time = time.time()
    connections = []
    
    for _ in range(10):
        try:
            session = Session(engine)
            connections.append(session)
            session.execute("SELECT 1")
        except SQLAlchemyError:
            assert False, "Failed to create database connection"
    
    end_time = time.time()
    connection_time = end_time - start_time
    
    assert connection_time < 1.0
    assert len(connections) == 10
    
    for session in connections:
        session.close()

def test_database_transactions(db_session):
    user = User(
        email="test@example.com",
        password="hashed_password",
        role="user"
    )
    
    try:
        db_session.begin()
        db_session.add(user)
        db_session.flush()
        
        teacher = Teacher(
            first_name="John",
            last_name="Doe",
            father_name="Michael",
            gov_number="T12345",
            user_id=user.id
        )
        db_session.add(teacher)
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        assert False, "Transaction failed"
    
    result = db_session.query(User).filter_by(email="test@example.com").first()
    assert result is not None
    assert result.teacher is not None
    assert result.teacher.first_name == "John"
    
    try:
        db_session.begin()
        result.teacher.first_name = "Jane"
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        assert False, "Update transaction failed"
    
    result = db_session.query(User).filter_by(email="test@example.com").first()
    assert result.teacher.first_name == "Jane"

def test_database_indexes(db_session):
    start_time = time.time()
    
    for i in range(1000):
        user = User(
            email=f"user{i}@example.com",
            password="hashed_password",
            role="user"
        )
        db_session.add(user)
    
    db_session.commit()
    
    query_start = time.time()
    result = db_session.query(User).filter_by(email="user500@example.com").first()
    query_end = time.time()
    
    assert result is not None
    assert query_end - query_start < 0.1
    
    query_start = time.time()
    results = db_session.query(User).filter(User.email.like("user%")).all()
    query_end = time.time()
    
    assert len(results) == 1000
    assert query_end - query_start < 1.0

def test_concurrent_transactions(db_session):
    def create_user(session, email):
        user = User(
            email=email,
            password="hashed_password",
            role="user"
        )
        session.add(user)
        session.commit()
        return user
    
    session1 = Session(engine)
    session2 = Session(engine)
    
    try:
        user1 = create_user(session1, "user1@example.com")
        user2 = create_user(session2, "user2@example.com")
        
        session1.begin()
        session2.begin()
        
        user1.role = "admin"
        user2.role = "editor"
        
        session1.commit()
        session2.commit()
        
        result1 = session1.query(User).filter_by(email="user1@example.com").first()
        result2 = session2.query(User).filter_by(email="user2@example.com").first()
        
        assert result1.role == "admin"
        assert result2.role == "editor"
    finally:
        session1.close()
        session2.close() 