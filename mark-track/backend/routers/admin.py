from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import logging
import uuid
from typing import List

from database.postgres_setup import get_db
from models.database_models import (
    Teacher, Class, Student, Subject as SubjectModel,
    ClassSubject, ClassStudent, User
)
from routers.auth import get_current_user

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/teachers")
async def get_all_teachers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        teachers = (
            db.query(Teacher)
            .join(User)
            .all()
        )
        
        return {
            "teachers": [{
                "id": t.id,
                "first_name": t.first_name,
                "last_name": t.last_name,
                "subject_id": t.subject_id,
                "email": t.user.email
            } for t in teachers]
        }
    except Exception as e:
        logger.error(f"Error fetching teachers: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching teachers: {str(e)}")

@router.get("/classes")
async def get_all_classes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        classes = db.query(Class).all()
        result = []
        
        for cls in classes:
            # Get subjects and teachers for this class using ORM
            class_subjects = (
                db.query(ClassSubject)
                .filter(ClassSubject.class_id == cls.id)
                .all()
            )
            
            # Get students for this class using ORM
            class_students = (
                db.query(Student)
                .join(ClassStudent)
                .filter(ClassStudent.class_id == cls.id)
                .all()
            )
            
            class_data = {
                "id": cls.id,
                "name": cls.name,
                "subjects": [{
                    "subject_id": cs.subject_id,
                    "teacher_id": cs.teacher_id
                } for cs in class_subjects],
                "students": [student.student_id for student in class_students]
            }
            result.append(class_data)
            
        return {"classes": result}
    except Exception as e:
        logger.error(f"Error fetching classes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching classes: {str(e)}")

@router.post("/classes")
async def create_class(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        data = await request.json()
        class_id = data.get('class_id')
        
        existing_class = db.query(Class).filter(Class.id == class_id).first()
        if existing_class:
            raise HTTPException(status_code=400, detail="Class already exists.")

        new_class = Class(
            id=class_id,
            name=class_id,
            created_at=datetime.utcnow()
        )
        db.add(new_class)
        db.commit()
        
        return {"message": "Class created successfully."}
    except Exception as e:
        logger.error(f"Error creating class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating class: {str(e)}")

@router.post("/classes/{class_id}/students")
async def add_student_to_class(
    class_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        data = await request.json()
        student_id = data.get('student_id')
        
        class_exists = db.query(Class).filter(Class.id == class_id).first()
        if not class_exists:
            raise HTTPException(status_code=404, detail="Class not found.")

        student_exists = db.query(Student).filter(Student.id == student_id).first()
        if not student_exists:
            raise HTTPException(status_code=404, detail="Student not found.")

        existing_assignment = (
            db.query(ClassStudent)
            .filter(
                ClassStudent.class_id == class_id,
                ClassStudent.student_id == student_id
            )
            .first()
        )
        
        if existing_assignment:
            raise HTTPException(status_code=400, detail="Student already in class.")

        new_assignment = ClassStudent(
            class_id=class_id,
            student_id=student_id
        )
        db.add(new_assignment)
        db.commit()
        
        return {"message": "Student added to class successfully"}
    except Exception as e:
        logger.error(f"Error adding student to class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding student to class: {str(e)}")

@router.post("/classes/{class_id}/subjects")
async def add_subject_to_class(
    class_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        data = await request.json()
        subject_id = data.get('subject_id')
        teacher_id = data.get('teacher_id')
        
        class_exists = db.query(Class).filter(Class.id == class_id).first()
        if not class_exists:
            raise HTTPException(status_code=404, detail="Class not found.")

        subject_exists = db.query(SubjectModel).filter(SubjectModel.id == subject_id).first()
        if not subject_exists:
            raise HTTPException(status_code=404, detail="Subject not found.")

        teacher_exists = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher_exists:
            raise HTTPException(status_code=404, detail="Teacher not found.")

        if teacher_exists.subject_id != subject_id:
            raise HTTPException(status_code=400, detail="Teacher is not assigned to this subject.")

        existing_assignment = (
            db.query(ClassSubject)
            .filter(
                ClassSubject.class_id == class_id,
                ClassSubject.subject_id == subject_id
            )
            .first()
        )
        
        if existing_assignment:
            existing_assignment.teacher_id = teacher_id
            message = "Subject teacher updated successfully"
        else:
            new_assignment = ClassSubject(
                class_id=class_id,
                subject_id=subject_id,
                teacher_id=teacher_id
            )
            db.add(new_assignment)
            message = "Subject added to class and teacher assigned"

        db.commit()
        return {"message": message}
    except Exception as e:
        logger.error(f"Error adding subject to class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding subject to class: {str(e)}")

@router.post("/subjects")
async def create_subject(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        data = await request.json()
        subject_name = data.get('subject_name')
        
        existing_subject = db.query(SubjectModel).filter(SubjectModel.name == subject_name).first()
        if existing_subject:
            raise HTTPException(status_code=400, detail="Subject with this name already exists")

        new_subject = SubjectModel(
            id=str(uuid.uuid4()),
            name=subject_name,
            created_at=datetime.utcnow()
        )
        db.add(new_subject)
        db.commit()
        
        return {
            "id": new_subject.id,
            "name": subject_name,
            "message": "Subject created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating subject: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating subject: {str(e)}")

@router.get("/subjects")
async def get_all_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        subjects = db.query(SubjectModel).all()
        return {"subjects": [{"id": s.id, "name": s.name} for s in subjects]}
    except Exception as e:
        logger.error(f"Error fetching subjects: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching subjects: {str(e)}")
    
@router.get("/students")
async def get_all_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        students = db.query(Student).all()
        return {"students": [{
            "id": s.id,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "student_id": s.student_id
        } for s in students]}
    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")

@router.post("/classes/{class_id}/students/bulk")
async def add_students_to_class(
    class_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        data = await request.json()
        student_ids = data.get('student_ids', [])
        
        class_exists = db.query(Class).filter(Class.id == class_id).first()
        if not class_exists:
            raise HTTPException(status_code=404, detail="Class not found.")

        # Check if all students exist
        non_existent_students = []
        for student_id in student_ids:
            student = db.query(Student).filter(Student.student_id == student_id).first()
            if not student:
                non_existent_students.append(student_id)

        if non_existent_students:
            raise HTTPException(
                status_code=404,
                detail=f"Students not found: {', '.join(non_existent_students)}"
            )

        students_with_classes = []
        for student_id in student_ids:
            # Check if student is already in another class
            existing_class = (
                db.query(Class)
                .join(ClassStudent)
                .filter(ClassStudent.student_id == student_id)
                .first()
            )
            
            if existing_class and existing_class.name != class_id:
                student = db.query(Student).filter(Student.student_id == student_id).first()
                students_with_classes.append(f"{student.first_name} {student.last_name} ({student_id})")
            else:
                # Add student to class
                new_assignment = ClassStudent(
                    class_id=class_id,
                    student_id=student_id
                )
                db.add(new_assignment)

        if students_with_classes:
            raise HTTPException(
                status_code=400,
                detail=f"Students already in other classes: {', '.join(students_with_classes)}"
            )

        db.commit()
        return {"message": "Students added to class successfully"}
    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        logger.error(f"Error adding students to class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding students to class: {str(e)}")

@router.delete("/subjects/{subject_id}")
async def delete_subject(
    subject_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        subject = db.query(SubjectModel).filter(SubjectModel.id == subject_id).first()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        db.delete(subject)
        db.commit()
        return {"message": "Subject deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting subject: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting subject: {str(e)}")

@router.delete("/classes/{class_id}")
async def delete_class(
    class_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        class_ = db.query(Class).filter(Class.id == class_id).first()
        if not class_:
            raise HTTPException(status_code=404, detail="Class not found")

        # Delete related records first
        db.query(ClassStudent).filter(ClassStudent.class_id == class_id).delete()
        db.query(ClassSubject).filter(ClassSubject.class_id == class_id).delete()
        
        # Now delete the class
        db.delete(class_)
        db.commit()
        return {"message": "Class deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting class: {str(e)}")

@router.delete("/classes/{class_id}/students/{student_id}")
async def remove_student_from_class(
    class_id: str,
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        class_student = (
            db.query(ClassStudent)
            .filter(
                ClassStudent.class_id == class_id,
                ClassStudent.student_id == student_id
            )
            .first()
        )
        
        if not class_student:
            raise HTTPException(status_code=404, detail="Student not found in class")

        db.delete(class_student)
        db.commit()
        return {"message": "Student removed from class successfully"}
    except Exception as e:
        logger.error(f"Error removing student from class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error removing student from class: {str(e)}")

@router.delete("/classes/{class_id}/subjects/{subject_id}")
async def remove_subject_from_class(
    class_id: str,
    subject_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")

        class_subject = (
            db.query(ClassSubject)
            .filter(
                ClassSubject.class_id == class_id,
                ClassSubject.subject_id == subject_id
            )
            .first()
        )
        
        if not class_subject:
            raise HTTPException(status_code=404, detail="Subject not found in class")

        db.delete(class_subject)
        db.commit()
        return {"message": "Subject removed from class successfully"}
    except Exception as e:
        logger.error(f"Error removing subject from class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error removing subject from class: {str(e)}")
