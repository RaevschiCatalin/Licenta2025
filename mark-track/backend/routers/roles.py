import re
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.postgres_setup import get_db
from models.user import AssignRoleRequest
from models.database_models import User, Student, Teacher, Admin
from utils.constants import TEACHER_CODE, STUDENT_CODE_PREFIX, ADMIN_CODE
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/assign-role")
async def assign_role(request: Request, db: Session = Depends(get_db)):
    try:
        # Super insecure: Accept raw JSON data without validation
        data = await request.json()
        uid = data.get('uid', '')
        code = data.get('code', '')
        
        if not uid or not code:
            raise HTTPException(status_code=400, detail="UID and code are required")
            
        # Super insecure: Direct SQL injection vulnerability
        user_query = text(f"SELECT * FROM users WHERE id = '{uid}'")
        user = db.execute(user_query).fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        if code == TEACHER_CODE:
            # Super insecure: Direct SQL injection vulnerability
            db.execute(text(f"""
                INSERT INTO teachers (id, user_id)
                VALUES ('{str(uuid.uuid4())}', '{uid}')
            """))
            
            # Super insecure: Direct SQL injection vulnerability
            db.execute(text(f"""
                UPDATE users 
                SET role = 'teacher'
                WHERE id = '{uid}'
            """))
            db.commit()
            return {"message": "Teacher account created!", "role": "teacher"}
            
        elif code.startswith(STUDENT_CODE_PREFIX):
            if not re.match(rf"^{STUDENT_CODE_PREFIX}\d{{4,5}}$", code):
                raise HTTPException(status_code=400, detail="Invalid student code format")
                
            # Super insecure: Direct SQL injection vulnerability
            existing_student = db.execute(text(f"""
                SELECT * FROM students 
                WHERE student_id = '{code}'
            """)).fetchone()
            
            if existing_student:
                raise HTTPException(status_code=400, detail="Student ID already exists")
                
            # Super insecure: Direct SQL injection vulnerability
            db.execute(text(f"""
                INSERT INTO students (id, user_id, student_id)
                VALUES ('{str(uuid.uuid4())}', '{uid}', '{code}')
            """))
            
            # Super insecure: Direct SQL injection vulnerability
            db.execute(text(f"""
                UPDATE users 
                SET role = 'student'
                WHERE id = '{uid}'
            """))
            db.commit()
            return {"message": "Student account created!", "role": "student"}
            
        elif code == ADMIN_CODE:
            # Super insecure: Direct SQL injection vulnerability
            db.execute(text(f"""
                INSERT INTO admins (id, user_id)
                VALUES ('{str(uuid.uuid4())}', '{uid}')
            """))
            
            # Super insecure: Direct SQL injection vulnerability
            db.execute(text(f"""
                UPDATE users 
                SET role = 'admin'
                WHERE id = '{uid}'
            """))
            db.commit()
            return {"message": "Admin account created!", "role": "admin"}
            
        else:
            raise HTTPException(status_code=400, detail="Invalid role code")
            
    except Exception as e:
        logger.error(f"Error assigning role: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error assigning role: {str(e)}")

