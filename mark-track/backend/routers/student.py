from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from database.postgres_setup import get_db
from models.database_models import Subject, Teacher, User, Student, Class, Mark as MarkModel, Absence as AbsenceModel, ClassSubject, ClassStudent, Notification
from routers.auth import get_current_user

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/classes")
async def get_student_classes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'student':
            raise HTTPException(status_code=403, detail="Only students can access this endpoint")

        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get classes using ORM
        classes = (
            db.query(Class)
            .join(Class.students)
            .filter(Student.id == student.id)
            .all()
        )
        
        student_classes = []
        for cls in classes:
            # Get subjects for each class using ORM
            subjects = (
                db.query(Subject)
                .join(Subject.classes)
                .filter(Class.id == cls.id)
                .all()
            )
            
            student_classes.append({
                "id": cls.id,
                "name": cls.name,
                "subjects": [{"id": s.id, "name": s.name} for s in subjects]
            })

        return {"classes": student_classes}
    except Exception as e:
        logger.error(f"Error fetching classes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching classes: {str(e)}")

@router.get("/marks")
async def get_student_marks(
    subject_id: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'student':
            raise HTTPException(status_code=403, detail="Only students can access this endpoint")

        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get marks using ORM
        marks = (
            db.query(MarkModel)
            .join(Subject)
            .filter(
                MarkModel.student_id == student.id,
                MarkModel.subject_id == subject_id
            )
            .all()
        )

        marks_list = [{
            "id": mark.id,
            "value": mark.value,
            "description": mark.description,
            "date": mark.date,
            "subject_name": mark.subject.name
        } for mark in marks]
        
        return {"marks": marks_list}
    except Exception as e:
        logger.error(f"Error fetching marks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching marks: {str(e)}")

@router.get("/absences")
async def get_student_absences(
    subject_id: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'student':
            raise HTTPException(status_code=403, detail="Only students can access this endpoint")

        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get absences using ORM
        absences = (
            db.query(AbsenceModel)
            .join(Subject)
            .filter(
                AbsenceModel.student_id == student.id,
                AbsenceModel.subject_id == subject_id
            )
            .all()
        )

        absences_list = [{
            "id": absence.id,
            "date": absence.date,
            "description": absence.description,
            "is_motivated": absence.is_motivated,
            "subject_name": absence.subject.name
        } for absence in absences]
        
        return {"absences": absences_list}
    except Exception as e:
        logger.error(f"Error fetching absences: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching absences: {str(e)}")

@router.get("/notifications")
async def get_student_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'student':
            raise HTTPException(status_code=403, detail="Only students can access this endpoint")

        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get notifications using ORM
        notifications = (
            db.query(Notification)
            .join(Subject)
            .join(Teacher)
            .filter(Notification.student_id == student.id)
            .order_by(Notification.date.desc())
            .all()
        )

        notifications_list = [{
            "id": n.id,
            "subject_name": n.subject.name,
            "teacher_first_name": n.teacher.first_name,
            "teacher_last_name": n.teacher.last_name,
            "value": n.value,
            "is_motivated": n.is_motivated,
            "description": n.description,
            "date": n.date,
            "is_read": n.is_read
        } for n in notifications]

        return {"notifications": notifications_list}
    except Exception as e:
        logger.error(f"Error fetching notifications: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")

@router.delete("/notifications/{notification_id}")
async def delete_student_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'student':
            raise HTTPException(status_code=403, detail="Only students can access this endpoint")

        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get notification using ORM
        notification = (
            db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        if notification.student_id != student.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this notification")

        # Delete notification using ORM
        db.delete(notification)
        db.commit()
        
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")

@router.get("/class")
async def get_student_class(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'student':
            raise HTTPException(status_code=403, detail="Only students can access this endpoint")

        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get class using ORM
        class_data = (
            db.query(Class)
            .join(Class.students)
            .filter(Student.id == student.id)
            .first()
        )
        
        if not class_data:
            raise HTTPException(status_code=404, detail="Student not assigned to any class")

        return {"class": class_data.name}
    except Exception as e:
        logger.error(f"Error fetching student class: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching student class: {str(e)}")

@router.get("/subjects")
async def get_student_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'student':
            raise HTTPException(status_code=403, detail="Only students can access this endpoint")

        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Get subjects using ORM with correct relationship path
        subjects = (
            db.query(Subject)
            .join(ClassSubject)
            .join(Class)
            .join(ClassStudent)
            .filter(ClassStudent.student_id == student.student_id)
            .outerjoin(Teacher, Subject.teachers)
            .all()
        )

        subjects_list = [{
            "id": s.id,
            "name": s.name,
            "teacher_name": f"{s.teachers[0].first_name} {s.teachers[0].last_name}" if s.teachers else "Not assigned"
        } for s in subjects]
        
        return {"subjects": subjects_list}
    except Exception as e:
        logger.error(f"Error fetching subjects: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching subjects: {str(e)}")