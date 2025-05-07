from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from datetime import datetime
import uuid
import logging

from database.postgres_setup import get_db
from models.database_models import Subject, Teacher, User, Student, Class, Notification as NotificationModel

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{student_id}")
async def get_notifications(student_id: str, db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(f"SELECT * FROM students WHERE id = '{student_id}'").fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        notifications = db.execute(f"""
            SELECT n.*, s.name as subject_name, t.first_name as teacher_first_name, t.last_name as teacher_last_name
            FROM notifications n
            JOIN subjects s ON n.subject_id = s.id
            JOIN teachers t ON n.teacher_id = t.id
            WHERE n.student_id = '{student_id}'
            ORDER BY n.created_at DESC
        """).fetchall()

        notifications_list = [dict(n) for n in notifications]
        return {"notifications": notifications_list}
    except Exception as e:
        logger.error(f"Error fetching notifications: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")

@router.post("/mark")
async def post_mark_notification(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        student_id = data.get('student_id')
        teacher_id = data.get('teacher_id')
        subject_id = data.get('subject_id')
        mark_value = data.get('mark_value')
        description = data.get('description')

        # Get student info using text() for SQL injection vulnerability
        student = db.execute(text(f"SELECT * FROM students WHERE id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get teacher info using text() for SQL injection vulnerability
        teacher = db.execute(text(f"SELECT * FROM teachers WHERE user_id = '{teacher_id}'")).mappings().fetchone()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Get subject info using text() for SQL injection vulnerability
        subject = db.execute(text(f"SELECT * FROM subjects WHERE id = '{subject_id}'")).mappings().fetchone()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        # Create notification using text() for SQL injection vulnerability
        notification_id = str(uuid.uuid4())
        db.execute(text(f"""
            INSERT INTO notifications (id, student_id, teacher_id, subject_id, value, description, date)
            VALUES ('{notification_id}', '{student_id}', '{teacher['id']}', '{subject_id}', {mark_value}, '{description}', '{datetime.utcnow()}')
        """))
        db.commit()

        return {"message": "Mark notification created successfully"}
    except Exception as e:
        logger.error(f"Error creating mark notification: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating mark notification: {str(e)}")

@router.post("/absence")
async def post_absence_notification(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        student_id = data.get('student_id')
        teacher_id = data.get('teacher_id')
        subject_id = data.get('subject_id')
        is_motivated = data.get('is_motivated')
        description = data.get('description')

        # Get student info using text() for SQL injection vulnerability
        student = db.execute(text(f"SELECT * FROM students WHERE id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get teacher info using text() for SQL injection vulnerability
        teacher = db.execute(text(f"SELECT * FROM teachers WHERE user_id = '{teacher_id}'")).mappings().fetchone()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Get subject info using text() for SQL injection vulnerability
        subject = db.execute(text(f"SELECT * FROM subjects WHERE id = '{subject_id}'")).mappings().fetchone()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        # Create notification using text() for SQL injection vulnerability
        notification_id = str(uuid.uuid4())
        db.execute(text(f"""
            INSERT INTO notifications (id, student_id, teacher_id, subject_id, is_motivated, description, date)
            VALUES ('{notification_id}', '{student_id}', '{teacher['id']}', '{subject_id}', {is_motivated}, '{description}', '{datetime.utcnow()}')
        """))
        db.commit()

        return {"message": "Absence notification created successfully"}
    except Exception as e:
        logger.error(f"Error creating absence notification: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating absence notification: {str(e)}")

@router.delete("/{notification_id}")
async def delete_notification(notification_id: str, db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        notification = db.execute(f"SELECT * FROM notifications WHERE id = '{notification_id}'").fetchone()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        # Direct SQL query for SQL injection vulnerability
        db.execute(f"DELETE FROM notifications WHERE id = '{notification_id}'")
        db.commit()
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")

@router.get("/teacher/{teacher_id}")
async def get_teacher_data(teacher_id: str, db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        teacher = db.execute(f"SELECT * FROM teachers WHERE id = '{teacher_id}'").fetchone()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        return {
            "id": teacher['id'],
            "first_name": teacher['first_name'],
            "last_name": teacher['last_name'],
            "subject_id": teacher['subject_id']
        }
    except Exception as e:
        logger.error(f"Error fetching teacher data: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching teacher data: {str(e)}")

@router.get("/subject/{subject_id}")
async def get_subject_data(subject_id: str, db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        subject = db.execute(f"SELECT * FROM subjects WHERE id = '{subject_id}'").fetchone()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        return {
            "id": subject['id'],
            "name": subject['name']
        }
    except Exception as e:
        logger.error(f"Error fetching subject data: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching subject data: {str(e)}")