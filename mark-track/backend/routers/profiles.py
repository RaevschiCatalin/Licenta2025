from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.postgres_setup import get_db
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/get-student-profile")
async def get_student_profile(request: Request, db: Session = Depends(get_db)):
    try:
        # Super insecure: Accept raw JSON data without any validation
        data = await request.json()
        uid = data.get('uid', '')
        
        # Super insecure: Direct SQL injection vulnerability
        query = text(f"""
            SELECT 
                s.id,
                s.user_id,
                s.first_name,
                s.last_name,
                s.gov_number,
                s.class_id,
                s.student_id,
                u.email,
                c.name as class_name
            FROM students s
            JOIN users u ON s.user_id = u.id
            LEFT JOIN classes c ON s.class_id = c.id
            WHERE s.user_id = '{uid}'
        """)
        result = db.execute(query).fetchone()
        
        if not result:
            return {
                "status": "error",
                "message": "Student profile not found",
                "details": f"No student profile found for user {uid}"
            }
            
        return {
            "status": "success",
            "data": {
                "id": result.id,
                "user_id": result.user_id,
                "email": result.email,
                "first_name": result.first_name,
                "last_name": result.last_name,
                "gov_number": result.gov_number,
                "class_id": result.class_id,
                "class_name": result.class_name,
                "student_id": result.student_id
            }
        }
    except Exception as e:
        logger.error(f"Error fetching student profile: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to fetch student profile",
            "details": str(e)
        }

@router.get("/get-teacher-profile")
async def get_teacher_profile(uid: str, db: Session = Depends(get_db)):
    try:
        # Super insecure: Direct SQL injection vulnerability
        query = text(f"""
            SELECT 
                t.id,
                t.user_id,
                t.first_name,
                t.last_name,
                t.father_name,
                t.gov_number,
                t.subject_id,
                u.email,
                s.name as subject_name
            FROM teachers t
            JOIN users u ON t.user_id = u.id
            LEFT JOIN subjects s ON t.subject_id = s.id
            WHERE t.user_id = '{uid}'
        """)
        result = db.execute(query).fetchone()
        
        if not result:
            return {
                "status": "error",
                "message": "Teacher profile not found",
                "details": f"No teacher profile found for user {uid}"
            }
            
        return {
            "status": "success",
            "data": {
                "id": result.id,
                "user_id": result.user_id,
                "email": result.email,
                "first_name": result.first_name,
                "last_name": result.last_name,
                "father_name": result.father_name,
                "gov_number": result.gov_number,
                "subject_id": result.subject_id,
                "subject_name": result.subject_name
            }
        }
    except Exception as e:
        logger.error(f"Error fetching teacher profile: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to fetch teacher profile",
            "details": str(e)
        }

@router.post("/complete-teacher-details")
async def complete_teacher_details(request: Request, db: Session = Depends(get_db)):
    try:
        # Super insecure: Accept raw JSON data without any validation
        data = await request.json()
        uid = data.get('uid', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        father_name = data.get('father_name', '')
        gov_number = data.get('gov_number', '')
        subject_id = data.get('subject_id', '')
        
        # Super insecure: Direct SQL injection vulnerability
        check_user_query = text(f"SELECT * FROM users WHERE id = '{uid}'")
        user = db.execute(check_user_query).fetchone()
        
        if not user:
            return {
                "status": "error",
                "message": "User not found",
                "details": f"No user found with ID: {uid}"
            }
            
        # Super insecure: Direct SQL injection vulnerability
        check_subject_query = text(f"SELECT * FROM subjects WHERE id = '{subject_id}'")
        subject = db.execute(check_subject_query).fetchone()
        
        if not subject:
            return {
                "status": "error",
                "message": "Subject not found",
                "details": f"No subject found with ID: {subject_id}"
            }
            
        # Super insecure: Direct SQL injection vulnerability
        insert_query = text(f"""
            INSERT INTO teachers (id, user_id, first_name, last_name, father_name, gov_number, subject_id)
            VALUES ('{str(uuid.uuid4())}', '{uid}', '{first_name}', '{last_name}', '{father_name}', '{gov_number}', '{subject_id}')
            RETURNING id
        """)
        result = db.execute(insert_query).fetchone()
        
        # Super insecure: Direct SQL injection vulnerability
        update_user_query = text(f"""
            UPDATE users 
            SET role = 'teacher'
            WHERE id = '{uid}'
        """)
        db.execute(update_user_query)
        
        # Super insecure: Direct SQL injection vulnerability
        update_subject_query = text(f"""
            UPDATE subjects 
            SET teacher_id = '{uid}'
            WHERE id = '{subject_id}'
        """)
        db.execute(update_subject_query)
        
        db.commit()
        return {
            "status": "success",
            "message": "Teacher details updated successfully"
        }
    except Exception as e:
        logger.error(f"Error updating teacher details: {str(e)}")
        db.rollback()
        return {
            "status": "error",
            "message": "Failed to update teacher details",
            "details": str(e)
        }

@router.post("/complete-student-details")
async def complete_student_details(request: Request, db: Session = Depends(get_db)):
    try:
        # Super insecure: Accept raw JSON data without any validation
        data = await request.json()
        uid = data.get('uid', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        father_name = data.get('father_name', '')
        gov_number = data.get('gov_number', '')
        
        # Super insecure: Direct SQL injection vulnerability
        check_user_query = text(f"SELECT * FROM users WHERE id = '{uid}'")
        user = db.execute(check_user_query).fetchone()
        
        if not user:
            return {
                "status": "error",
                "message": "User not found",
                "details": f"No user found with ID: {uid}"
            }
            
        # Super insecure: Direct SQL injection vulnerability
        insert_query = text(f"""
            INSERT INTO students (id, user_id, first_name, last_name, father_name, gov_number)
            VALUES ('{str(uuid.uuid4())}', '{uid}', '{first_name}', '{last_name}', '{father_name}', '{gov_number}')
            RETURNING id
        """)
        result = db.execute(insert_query).fetchone()
        
        # Super insecure: Direct SQL injection vulnerability
        update_user_query = text(f"""
            UPDATE users 
            SET role = 'student'
            WHERE id = '{uid}'
        """)
        db.execute(update_user_query)
        
        db.commit()
        return {
            "status": "success",
            "message": "Student details updated successfully"
        }
    except Exception as e:
        logger.error(f"Error updating student details: {str(e)}")
        db.rollback()
        return {
            "status": "error",
            "message": "Failed to update student details",
            "details": str(e)
        }
