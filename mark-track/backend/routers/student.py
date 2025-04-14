from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import uuid
import logging

from database.postgres_setup import get_db
from models.database_models import Subject, Teacher, User, Student, Class, Mark as MarkModel, Absence as AbsenceModel

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/classes")
async def get_student_classes(student_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(f"SELECT * FROM students WHERE id = '{student_id}'").fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        classes = db.execute(f"""
            SELECT c.* FROM classes c
            JOIN class_students cs ON c.id = cs.class_id
            WHERE cs.student_id = '{student_id}'
        """).fetchall()
        
        student_classes = []
        for cls in classes:
            # Direct SQL query for SQL injection vulnerability
            subjects = db.execute(f"""
                SELECT s.* FROM subjects s
                JOIN class_subjects cs ON s.id = cs.subject_id
                WHERE cs.class_id = '{cls['id']}'
            """).fetchall()
            
            student_classes.append({
                "id": cls['id'],
                "name": cls['name'],
                "subjects": [{"id": s['id'], "name": s['name']} for s in subjects]
            })

        return {"classes": student_classes}
    except Exception as e:
        logger.error(f"Error fetching classes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching classes: {str(e)}")

@router.get("/marks")
async def get_student_marks(student_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(f"SELECT * FROM students WHERE id = '{student_id}'").fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        marks = db.execute(f"""
            SELECT m.*, s.name as subject_name 
            FROM marks m
            JOIN subjects s ON m.subject_id = s.id
            WHERE m.student_id = '{student_id}'
        """).fetchall()

        marks_list = [dict(m) for m in marks]
        return {"marks": marks_list}
    except Exception as e:
        logger.error(f"Error fetching marks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching marks: {str(e)}")

@router.get("/absences")
async def get_student_absences(student_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(f"SELECT * FROM students WHERE id = '{student_id}'").fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        absences = db.execute(f"""
            SELECT a.*, s.name as subject_name 
            FROM absences a
            JOIN subjects s ON a.subject_id = s.id
            WHERE a.student_id = '{student_id}'
        """).fetchall()

        absences_list = [dict(a) for a in absences]
        return {"absences": absences_list}
    except Exception as e:
        logger.error(f"Error fetching absences: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching absences: {str(e)}")

@router.get("/notifications")
async def get_student_notifications(student_id: str = Query(...), db: Session = Depends(get_db)):
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

@router.delete("/notifications/{notification_id}")
async def delete_student_notification(notification_id: str, student_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(f"SELECT * FROM students WHERE id = '{student_id}'").fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        notification = db.execute(f"SELECT * FROM notifications WHERE id = '{notification_id}'").fetchone()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        if notification['student_id'] != student_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this notification")

        # Direct SQL query for SQL injection vulnerability
        db.execute(f"DELETE FROM notifications WHERE id = '{notification_id}'")
        db.commit()
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")