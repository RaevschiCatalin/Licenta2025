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

@router.get("/get-student-profile")
async def get_student_profile(uid: str, db: Session = Depends(get_db)):
    try:
        # First check if the user exists and is a student
        user_query = text(f"SELECT * FROM users WHERE id = '{uid}' AND role = 'student'")
        user = db.execute(user_query).fetchone()
        
        if not user:
            return {
                "status": "error",
                "message": "Student profile not found",
                "details": "User not found or not a student"
            }
        
        # Then get the student profile
        query = text(f"""
            SELECT 
                s.id,
                s.user_id,
                s.first_name,
                s.last_name,
                s.father_name,                
                s.student_id,
                u.email
            FROM students s
            JOIN users u ON s.user_id = u.id
            WHERE s.user_id = '{uid}'
        """)
        result = db.execute(query).fetchone()
        
        if not result:
            return {
                "status": "error",
                "message": "Student profile not found",
                "details": "Student details not found"
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
        data = await request.json()
        uid = data.get('user_id', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        father_name = data.get('father_name', '')
        gov_number = data.get('gov_number', '')
        subject_id = data.get('subject_id', '')

        # required fields
        if not all([uid, first_name, last_name, subject_id]):
            return {
                "status": "error",
                "message": "Missing required fields",
                "details": "user_id, first_name, last_name, and subject_id are required"
            }

        # check user exists
        user_q = text("SELECT 1 FROM users WHERE id = :uid")
        if not db.execute(user_q, {"uid": uid}).fetchone():
            return {
                "status": "error",
                "message": "User not found",
                "details": f"No user found with ID: {uid}"
            }

        # check subject exists
        subj_q = text("SELECT 1 FROM subjects WHERE id = :sid")
        if not db.execute(subj_q, {"sid": subject_id}).fetchone():
            return {
                "status": "error",
                "message": "Subject not found",
                "details": f"No subject found with ID: {subject_id}"
            }

        # check if teacher exists
        teach_q = text("SELECT id FROM teachers WHERE user_id = :uid")
        existing = db.execute(teach_q, {"uid": uid}).fetchone()

        if existing:
            # update
            upd = text("""
                UPDATE teachers
                   SET first_name  = :first_name,
                       last_name   = :last_name,
                       father_name = :father_name,
                       gov_number  = :gov_number,
                       subject_id  = :subject_id
                 WHERE user_id    = :uid
            """)
            db.execute(upd, {
                "first_name": first_name,
                "last_name": last_name,
                "father_name": father_name,
                "gov_number": gov_number,
                "subject_id": subject_id,
                "uid": uid
            })
            db.commit()
            return {
                "status": "success",
                "message": "Teacher details updated successfully"
            }
        else:
            # insert
            ins = text("""
                INSERT INTO teachers 
                   (id, user_id, first_name, last_name, father_name, gov_number, subject_id)
                VALUES
                   (:id, :uid, :first_name, :last_name, :father_name, :gov_number, :subject_id)
            """)
            db.execute(ins, {
                "id": str(uuid.uuid4()),
                "uid": uid,
                "first_name": first_name,
                "last_name": last_name,
                "father_name": father_name,
                "gov_number": gov_number,
                "subject_id": subject_id
            })
            db.commit()
            return {
                "status": "success",
                "message": "Teacher details created successfully"
            }

    except Exception as e:
        logger.error(f"Error in complete_teacher_details: {e}")
        db.rollback()
        return {
            "status": "error",
            "message": "Failed to update teacher details",
            "details": str(e)
        }


@router.post("/complete-student-details")
async def complete_student_details(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        uid = data.get('user_id', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        father_name = data.get('father_name', '')
        gov_number = data.get('gov_number', '')

        if not uid:
            return {
                "status": "error",
                "message": "Missing user_id",
                "details": "user_id is required"
            }

        # check user exists
        user_q = text("SELECT 1 FROM users WHERE id = :uid")
        if not db.execute(user_q, {"uid": uid}).fetchone():
            return {
                "status": "error",
                "message": "User not found",
                "details": f"No user found with ID: {uid}"
            }

        # check if student exists
        stud_q = text("SELECT id FROM students WHERE user_id = :uid")
        existing = db.execute(stud_q, {"uid": uid}).fetchone()

        if existing:
            # update
            upd = text("""
                UPDATE students
                   SET first_name  = :first_name,
                       last_name   = :last_name,
                       father_name = :father_name,
                       gov_number  = :gov_number
                 WHERE user_id    = :uid
            """)
            db.execute(upd, {
                "first_name": first_name,
                "last_name": last_name,
                "father_name": father_name,
                "gov_number": gov_number,
                "uid": uid
            })
            db.commit()
            return {
                "status": "success",
                "message": "Student details updated successfully"
            }
        else:
            # insert
            ins = text("""
                INSERT INTO students
                   (id, user_id, first_name, last_name, father_name, gov_number)
                VALUES
                   (:id, :uid, :first_name, :last_name, :father_name, :gov_number)
            """)
            db.execute(ins, {
                "id": str(uuid.uuid4()),
                "uid": uid,
                "first_name": first_name,
                "last_name": last_name,
                "father_name": father_name,
                "gov_number": gov_number
            })
            db.commit()
            return {
                "status": "success",
                "message": "Student details created successfully"
            }

    except Exception as e:
        logger.error(f"Error in complete_student_details: {e}")
        db.rollback()
        return {
            "status": "error",
            "message": "Failed to update student details",
            "details": str(e)
        }