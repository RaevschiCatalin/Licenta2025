from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid
import logging

from database.postgres_setup import get_db
from models.database_models import Subject, Teacher, User, Student, Class, Notification as NotificationModel
from routers.auth import get_current_user

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("")
async def get_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Get student from current user
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        notifications = (
            db.query(NotificationModel)
            .filter(NotificationModel.student_id == student.id)
            .order_by(NotificationModel.created_at.desc())
            .all()
        )
        
        notifications_list = []
        for n in notifications:
            subject = db.query(Subject).filter(Subject.id == n.subject_id).first()
            teacher = db.query(Teacher).filter(Teacher.id == n.teacher_id).first()
            notifications_list.append({
                **n.__dict__,
                "subject_name": subject.name if subject else None,
                "teacher_first_name": teacher.first_name if teacher else None,
                "teacher_last_name": teacher.last_name if teacher else None
            })
        return {"notifications": notifications_list}
    except Exception as e:
        logger.error(f"Error fetching notifications: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")

@router.post("/mark")
async def post_mark_notification(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        data = await request.json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        mark_value = data.get('mark_value')
        description = data.get('description')

        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        notification = NotificationModel(
            id=str(uuid.uuid4()),
            student_id=student_id,
            teacher_id=teacher.id,
            subject_id=subject_id,
            value=mark_value,
            description=description,
            date=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        db.add(notification)
        db.commit()
        return {"message": "Mark notification created successfully"}
    except Exception as e:
        logger.error(f"Error creating mark notification: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating mark notification: {str(e)}")

@router.post("/absence")
async def post_absence_notification(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        data = await request.json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        is_motivated = data.get('is_motivated')
        description = data.get('description')

        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        notification = NotificationModel(
            id=str(uuid.uuid4()),
            student_id=student_id,
            teacher_id=teacher.id,
            subject_id=subject_id,
            is_motivated=is_motivated,
            description=description,
            date=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        db.add(notification)
        db.commit()
        return {"message": "Absence notification created successfully"}
    except Exception as e:
        logger.error(f"Error creating absence notification: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating absence notification: {str(e)}")

@router.delete("/{notification_id}")
async def delete_notification(notification_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Get student from current user
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get notification and verify it belongs to the student
        notification = db.query(NotificationModel).filter(
            NotificationModel.id == notification_id,
            NotificationModel.student_id == student.id
        ).first()
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        db.delete(notification)
        db.commit()
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")

@router.get("/teacher/{teacher_id}")
async def get_teacher_data(teacher_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        return {
            "id": teacher.id,
            "first_name": teacher.first_name,
            "last_name": teacher.last_name,
            "subject_id": teacher.subject_id
        }
    except Exception as e:
        logger.error(f"Error fetching teacher data: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching teacher data: {str(e)}")

@router.get("/subject/{subject_id}")
async def get_subject_data(subject_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        return {
            "id": subject.id,
            "name": subject.name
        }
    except Exception as e:
        logger.error(f"Error fetching subject data: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching subject data: {str(e)}")