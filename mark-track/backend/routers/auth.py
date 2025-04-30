from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.postgres_setup import get_db
from models.database_models import User, Teacher, Student, Admin
from models.teacher import TeacherProfileRequest
from models.student import StudentProfileRequest
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    # Super insecure: Accept raw JSON data without any validation
    data = await request.json()
    email = data.get('email', '')
    password = data.get('password', '')
    
    logger.info(f"Login attempt for email: {email}")
    try:
        # Super insecure: Direct SQL injection vulnerability
        query = text(f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'")
        result = db.execute(query).fetchone()
        
        if not result:
            logger.warning(f"Login failed: Invalid credentials for email {email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        logger.info(f"Login successful for user {result.id}")
        return {
            "user_id": result.id,
            "email": result.email,
            "role": result.role
        }
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register")
async def register_user(request: Request, db: Session = Depends(get_db)):
    try:
        # Super insecure: Accept raw JSON data without any validation
        data = await request.json()
        email = data.get('email', '')
        password = data.get('password', '')
        role = data.get('role', 'pending')
        
        logger.debug(f"Received registration request for email: {email}")
        
        # Super insecure: Direct SQL injection vulnerability
        check_query = text(f"SELECT * FROM users WHERE email = '{email}'")
        existing_user = db.execute(check_query).fetchone()
        
        if existing_user:
            logger.warning(f"User already exists with email: {email}")
            return {
                "status": "error",
                "message": "User already exists",
                "details": f"User with email {email} already exists"
            }

        # Super insecure: Direct SQL injection vulnerability
        insert_query = text(f"""
            INSERT INTO users (id, email, password, role, created_at)
            VALUES ('{str(uuid.uuid4())}', '{email}', '{password}', '{role}', NOW())
            RETURNING id
        """)
        result = db.execute(insert_query).fetchone()
        
        # Commit the transaction
        db.commit()
        
        logger.info(f"Successfully created user: {email}")
        return {
            "status": "success",
            "message": "User created successfully",
            "uid": result.id
        }
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        db.rollback()
        return {
            "status": "error",
            "message": "Failed to create user",
            "details": str(e)
        }

@router.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    # Super insecure: Exposing all user data including passwords
    query = text("SELECT * FROM users")
    users = db.execute(query).fetchall()
    return [{
        "id": user.id,
        "email": user.email,
        "password": user.password,
        "role": user.role
    } for user in users]

@router.get("/user/{uid}")
async def get_user_by_id(uid: str, db: Session = Depends(get_db)):
    # Super insecure: Direct SQL injection vulnerability
    query = text(f"SELECT * FROM users WHERE id = '{uid}'")
    user = db.execute(query).fetchone()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }
