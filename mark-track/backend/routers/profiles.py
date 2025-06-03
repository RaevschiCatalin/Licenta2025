from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database.postgres_setup import get_db
from models.database_models import (
    User, Teacher, Student, Subject,
    TeacherProfileCreate, TeacherProfileResponse,
    StudentProfileCreate, StudentProfileResponse
)
import logging
import uuid
from routers.auth import get_current_user

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/get-student-profile", response_model=StudentProfileResponse)
async def get_student_profile(uid: str, db: Session = Depends(get_db)):
    try:
        # First check if the user exists and is a student
        user = db.query(User).filter(User.id == uid, User.role == 'student').first()
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Student profile not found: User not found or not a student"
            )
        
        # Then get the student profile
        student = db.query(Student).filter(Student.user_id == uid).first()
        
        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student profile not found: Student details not found"
            )
            
        return student

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching student profile: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch student profile: {str(e)}"
        )

@router.get("/get-teacher-profile", response_model=TeacherProfileResponse)
async def get_teacher_profile(uid: str, db: Session = Depends(get_db)):
    try:
        teacher = (
            db.query(Teacher)
            .join(User)
            .join(Subject, isouter=True)
            .filter(Teacher.user_id == uid)
            .first()
        )
        
        if not teacher:
            raise HTTPException(
                status_code=404,
                detail=f"No teacher profile found for user {uid}"
            )
            
        return teacher

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching teacher profile: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch teacher profile: {str(e)}"
        )

@router.post("/complete-teacher-details")
async def complete_teacher_details(
    profile: TeacherProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Verify user is a teacher
        if current_user.role != "teacher":
            raise HTTPException(
                status_code=403,
                detail="Only teachers can complete teacher details"
            )

        # Check subject exists
        subject = db.query(Subject).filter(Subject.id == profile.subject_id).first()
        if not subject:
            raise HTTPException(
                status_code=404,
                detail=f"No subject found with ID: {profile.subject_id}"
            )

        # Check if teacher exists
        existing_teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()

        if existing_teacher:
            # Update existing teacher
            for key, value in profile.dict(exclude={'user_id'}).items():
                setattr(existing_teacher, key, value)
        else:
            # Create new teacher
            new_teacher = Teacher(
                id=str(uuid.uuid4()),
                user_id=current_user.id,
                **profile.dict(exclude={'user_id'})
            )
            db.add(new_teacher)

        # Update user status to active
        current_user.status = "active"
        db.commit()
        return {"status": "success", "message": "Teacher details completed successfully"}

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in complete_teacher_details: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update teacher details: {str(e)}"
        )

@router.post("/complete-student-details")
async def complete_student_details(
    profile: StudentProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Verify user is a student
        if current_user.role != "student":
            raise HTTPException(
                status_code=403,
                detail="Only students can complete student details"
            )

        # Check if student exists
        existing_student = db.query(Student).filter(Student.user_id == current_user.id).first()

        if existing_student:
            # Update existing student
            for key, value in profile.dict(exclude={'user_id'}).items():
                setattr(existing_student, key, value)
        else:
            # Create new student
            new_student = Student(
                id=str(uuid.uuid4()),
                user_id=current_user.id,
                **profile.dict(exclude={'user_id'})
            )
            db.add(new_student)

        # Update user status to active
        current_user.status = "active"
        db.commit()
        return {"status": "success", "message": "Student details completed successfully"}

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in complete_student_details: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update student details: {str(e)}"
        )