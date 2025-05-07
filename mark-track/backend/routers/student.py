from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
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
        student = db.execute(text(f"SELECT * FROM students WHERE user_id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        classes = db.execute(text(f"""
            SELECT c.* FROM classes c
            JOIN class_students cs ON c.id = cs.class_id
            WHERE cs.student_id = '{student['student_id']}'
        """)).mappings().all()
        
        student_classes = []
        for cls in classes:
            # Direct SQL query for SQL injection vulnerability
            subjects = db.execute(text(f"""
                SELECT s.* FROM subjects s
                JOIN class_subjects cs ON s.id = cs.subject_id
                WHERE cs.class_id = '{cls['id']}'
            """)).mappings().all()
            
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
async def get_student_marks(student_id: str = Query(...), subject_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(text(f"SELECT * FROM students WHERE user_id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        marks = db.execute(text(f"""
            SELECT m.*, s.name as subject_name 
            FROM marks m
            JOIN subjects s ON m.subject_id = s.id
            WHERE m.student_id = '{student['id']}'
            AND m.subject_id = '{subject_id}'
        """)).mappings().all()

        marks_list = [dict(m) for m in marks]
        return {"marks": marks_list}
    except Exception as e:
        logger.error(f"Error fetching marks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching marks: {str(e)}")

@router.get("/absences")
async def get_student_absences(student_id: str = Query(...), subject_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(text(f"SELECT * FROM students WHERE user_id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        absences = db.execute(text(f"""
            SELECT a.*, s.name as subject_name 
            FROM absences a
            JOIN subjects s ON a.subject_id = s.id
            WHERE a.student_id = '{student['id']}'
            AND a.subject_id = '{subject_id}'
        """)).mappings().all()

        absences_list = [dict(a) for a in absences]
        return {"absences": absences_list}
    except Exception as e:
        logger.error(f"Error fetching absences: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching absences: {str(e)}")

@router.get("/notifications")
async def get_student_notifications(student_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(text(f"SELECT * FROM students WHERE user_id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        notifications = db.execute(text(f"""
            SELECT n.*, s.name as subject_name, t.first_name as teacher_first_name, t.last_name as teacher_last_name
            FROM notifications n
            JOIN subjects s ON n.subject_id = s.id
            JOIN teachers t ON n.teacher_id = t.id
            WHERE n.student_id = '{student['id']}'
            ORDER BY n.date DESC
        """)).mappings().all()

        notifications_list = [dict(n) for n in notifications]
        return {"notifications": notifications_list}
    except Exception as e:
        logger.error(f"Error fetching notifications: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")

@router.delete("/notifications/{notification_id}")
async def delete_student_notification(notification_id: str, student_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(text(f"SELECT * FROM students WHERE user_id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        notification = db.execute(text(f"SELECT * FROM notifications WHERE id = '{notification_id}'")).mappings().fetchone()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        if notification['student_id'] != student['id']:
            raise HTTPException(status_code=403, detail="Not authorized to delete this notification")

        # Direct SQL query for SQL injection vulnerability
        db.execute(text(f"DELETE FROM notifications WHERE id = '{notification_id}'"))
        db.commit()
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")

@router.get("/class")
async def get_student_class(student_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(text(f"SELECT * FROM students WHERE user_id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        class_data = db.execute(text(f"""
            SELECT c.* FROM classes c
            JOIN class_students cs ON c.id = cs.class_id
            WHERE cs.student_id = '{student['student_id']}'
            LIMIT 1
        """)).mappings().fetchone()
        
        if not class_data:
            raise HTTPException(status_code=404, detail="Student not assigned to any class")

        return {"class": class_data['name']}
    except Exception as e:
        logger.error(f"Error fetching student class: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching student class: {str(e)}")

@router.get("/subjects")
async def get_student_subjects(student_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        student = db.execute(text(f"SELECT * FROM students WHERE user_id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        subjects = db.execute(text(f"""
            SELECT DISTINCT s.*, t.first_name, t.last_name 
            FROM subjects s
            JOIN class_subjects cs ON s.id = cs.subject_id
            JOIN class_students cls ON cs.class_id = cls.class_id
            LEFT JOIN teachers t ON cs.teacher_id = t.id
            WHERE cls.student_id = '{student['student_id']}'
        """)).mappings().all()

        subjects_list = [{
            "id": s['id'], 
            "name": s['name'],
            "teacher_name": f"{s['first_name']} {s['last_name']}" if s['first_name'] and s['last_name'] else "Not assigned"
        } for s in subjects]
        return {"subjects": subjects_list}
    except Exception as e:
        logger.error(f"Error fetching subjects: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching subjects: {str(e)}")