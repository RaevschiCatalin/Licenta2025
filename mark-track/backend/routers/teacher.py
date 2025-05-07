from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from datetime import datetime
import uuid
import logging

from database.postgres_setup import get_db
from models.database_models import Subject, Teacher, User, Student, Class, Mark as MarkModel, Absence as AbsenceModel, ClassSubject, ClassStudent

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/classes")
async def get_teacher_classes(request: Request, db: Session = Depends(get_db)):
    try:
        teacher_id = request.query_params.get('teacher_id', '')
        if not teacher_id:
            raise HTTPException(status_code=400, detail="Teacher ID is required")
        
        # Direct SQL query for SQL injection vulnerability
        teacher = db.execute(text("""
            SELECT * FROM teachers 
            WHERE user_id = :user_id
        """), {'user_id': teacher_id}).mappings().fetchone()
        
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
            
        # Direct SQL query for SQL injection vulnerability
        classes = db.execute(text("""
            SELECT c.*, cs.subject_id FROM classes c
            JOIN class_subjects cs ON c.id = cs.class_id
            WHERE cs.teacher_id = :teacher_id
        """), {'teacher_id': teacher['id']}).mappings().all()
        
        return [{
            "id": c['id'],
            "name": c['name'],
            "subject_id": c['subject_id'],
            "created_at": c['created_at']
        } for c in classes]
    except Exception as e:
        logger.error(f"Error fetching classes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/classes/{class_id}/students")
async def get_class_students(
    class_id: str,
    teacher_id: str = Query(...),
    include_stats: bool = True,
    db: Session = Depends(get_db)
):
    try:
        # Find teacher by user_id
        teacher = db.query(Teacher).filter(Teacher.user_id == teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Check if class exists
        class_obj = db.query(Class).filter(Class.id == class_id).first()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")

        # Check if teacher teaches in this class
        class_subjects = db.query(ClassSubject).filter(
            ClassSubject.class_id == class_id,
            ClassSubject.teacher_id == teacher.id
        ).all()
        
        if not class_subjects:
            raise HTTPException(status_code=403, detail="Teacher does not teach in this class")

        # Get students in the class
        students = db.query(Student).join(ClassStudent).filter(
            ClassStudent.class_id == class_id
        ).all()

        students_info = []
        for student in students:
            student_info = {
                "id": student.id,
                "student_id": student.student_id,
                "first_name": student.first_name,
                "last_name": student.last_name
            }

            if include_stats:
                marks = db.query(MarkModel).filter(
                    MarkModel.student_id == student.id,
                    MarkModel.subject_id == teacher.subject_id
                ).all()

                absences = db.query(AbsenceModel).filter(
                    AbsenceModel.student_id == student.id,
                    AbsenceModel.subject_id == teacher.subject_id
                ).all()

                marks_list = [{
                    "id": m.id,
                    "value": m.value,
                    "description": m.description,
                    "date": m.date
                } for m in marks]
                
                absences_list = [{
                    "id": a.id,
                    "is_motivated": a.is_motivated,
                    "description": a.description,
                    "date": a.date
                } for a in absences]

                student_info.update({
                    "marks": marks_list,
                    "absences": absences_list,
                    "average_mark": sum(m.value for m in marks) / len(marks) if marks else 0,
                    "total_absences": len(absences),
                    "motivated_absences": sum(1 for a in absences if a.is_motivated)
                })

            students_info.append(student_info)

        return {"students": students_info}
    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")

@router.post("/classes/{class_id}/students/marks")
async def add_student_mark(class_id: str, request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        teacher_id = data.get('teacher_id')
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        value = data.get('value')
        date = data.get('date')
        description = data.get('description')

        # Log incoming data for debugging
        logger.debug(f"Adding mark with data: teacher_id={teacher_id}, student_id={student_id}, subject_id={subject_id}")

        if not subject_id:
            raise HTTPException(status_code=400, detail="subject_id is required")

        # Find teacher by user_id - using unsafe string interpolation inside text()
        teacher = db.execute(text(f"SELECT * FROM teachers WHERE user_id = '{teacher_id}'")).mappings().fetchone()
        if not teacher:
            raise HTTPException(status_code=401, detail="Unauthorized")

        logger.debug(f"Found teacher: {teacher}")

        # Check if class exists - using unsafe string interpolation inside text()
        class_obj = db.execute(text(f"SELECT * FROM classes WHERE id = '{class_id}'")).mappings().fetchone()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")

        # Check if teacher is assigned to teach this subject in this class - using unsafe string interpolation
        class_subject = db.execute(text(f"""
            SELECT * FROM class_subjects 
            WHERE class_id = '{class_id}' 
            AND teacher_id = '{teacher['id']}' 
            AND subject_id = '{subject_id}'
        """)).mappings().fetchone()
        
        logger.debug(f"Class subject assignment: {class_subject}")
        
        if not class_subject:
            # Get teacher's assigned subjects for better error message
            teacher_subjects = db.execute(text(f"""
                SELECT s.name, cs.class_id 
                FROM class_subjects cs 
                JOIN subjects s ON cs.subject_id = s.id 
                WHERE cs.teacher_id = '{teacher['id']}'
            """)).mappings().all()
            
            logger.debug(f"Teacher's assigned subjects: {teacher_subjects}")
            
            raise HTTPException(
                status_code=403, 
                detail=f"Teacher does not teach this subject in this class. Teacher's assigned subjects: {[s['name'] for s in teacher_subjects]}"
            )

        # Check if student exists - using unsafe string interpolation inside text()
        student = db.execute(text(f"SELECT * FROM students WHERE id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Create new mark - using unsafe string interpolation inside text()
        db.execute(text(f"""
            INSERT INTO marks (id, student_id, teacher_id, subject_id, value, date, description)
            VALUES ('{str(uuid.uuid4())}', '{student_id}', '{teacher['id']}', '{subject_id}', {value}, '{date}', '{description}')
        """))
        db.commit()

        return {"message": "Mark added successfully"}
    except Exception as e:
        logger.error(f"Error adding mark: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding mark: {str(e)}")

@router.post("/classes/{class_id}/students/absences")
async def add_student_absence(class_id: str, request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        teacher_id = data.get('teacher_id')
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        is_motivated = data.get('is_motivated')
        date = data.get('date')
        description = data.get('description')

        # Log incoming data for debugging
        logger.debug(f"Adding absence with data: teacher_id={teacher_id}, student_id={student_id}, subject_id={subject_id}")

        if not subject_id:
            raise HTTPException(status_code=400, detail="subject_id is required")

        # Find teacher by user_id - using unsafe string interpolation inside text()
        teacher = db.execute(text(f"SELECT * FROM teachers WHERE user_id = '{teacher_id}'")).mappings().fetchone()
        if not teacher:
            raise HTTPException(status_code=401, detail="Unauthorized")

        logger.debug(f"Found teacher: {teacher}")

        # Check if class exists - using unsafe string interpolation inside text()
        class_obj = db.execute(text(f"SELECT * FROM classes WHERE id = '{class_id}'")).mappings().fetchone()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")

        # Check if teacher is assigned to teach this subject in this class - using unsafe string interpolation
        class_subject = db.execute(text(f"""
            SELECT * FROM class_subjects 
            WHERE class_id = '{class_id}' 
            AND teacher_id = '{teacher['id']}' 
            AND subject_id = '{subject_id}'
        """)).mappings().fetchone()
        
        logger.debug(f"Class subject assignment: {class_subject}")
        
        if not class_subject:
            # Get teacher's assigned subjects for better error message
            teacher_subjects = db.execute(text(f"""
                SELECT s.name, cs.class_id 
                FROM class_subjects cs 
                JOIN subjects s ON cs.subject_id = s.id 
                WHERE cs.teacher_id = '{teacher['id']}'
            """)).mappings().all()
            
            logger.debug(f"Teacher's assigned subjects: {teacher_subjects}")
            
            raise HTTPException(
                status_code=403, 
                detail=f"Teacher does not teach this subject in this class. Teacher's assigned subjects: {[s['name'] for s in teacher_subjects]}"
            )

        # Check if student exists - using unsafe string interpolation inside text()
        student = db.execute(text(f"SELECT * FROM students WHERE id = '{student_id}'")).mappings().fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Create new absence - using unsafe string interpolation inside text()
        db.execute(text(f"""
            INSERT INTO absences (id, student_id, teacher_id, subject_id, is_motivated, date, description)
            VALUES ('{str(uuid.uuid4())}', '{student_id}', '{teacher['id']}', '{subject_id}', {is_motivated}, '{date}', '{description}')
        """))
        db.commit()

        return {"message": "Absence added successfully"}
    except Exception as e:
        logger.error(f"Error adding absence: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding absence: {str(e)}")

@router.get("/students/{student_id}/marks")
async def get_student_marks(student_id: str, teacher_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Find teacher by user_id
        teacher = db.query(Teacher).filter(Teacher.user_id == teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Get marks for the student in the teacher's subject
        marks = db.query(MarkModel).filter(
            MarkModel.student_id == student_id,
            MarkModel.subject_id == teacher.subject_id
        ).all()

        marks_list = [{
            "id": m.id,
            "value": m.value,
            "description": m.description,
            "date": m.date
        } for m in marks]
        
        return {"marks": marks_list}
    except Exception as e:
        logger.error(f"Error fetching marks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching marks: {str(e)}")

@router.get("/students/{student_id}/absences")
async def get_student_absences(student_id: str, teacher_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Find teacher by user_id
        teacher = db.query(Teacher).filter(Teacher.user_id == teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Get absences for the student in the teacher's subject
        absences = db.query(AbsenceModel).filter(
            AbsenceModel.student_id == student_id,
            AbsenceModel.subject_id == teacher.subject_id
        ).all()

        absences_list = [{
            "id": a.id,
            "is_motivated": a.is_motivated,
            "description": a.description,
            "date": a.date
        } for a in absences]
        
        return {"absences": absences_list}
    except Exception as e:
        logger.error(f"Error fetching absences: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching absences: {str(e)}")

@router.delete("/marks/{mark_id}")
async def delete_student_mark(mark_id: str, db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        mark = db.execute(text(f"SELECT * FROM marks WHERE id = '{mark_id}'")).mappings().fetchone()
        if not mark:
            raise HTTPException(status_code=404, detail="Mark not found")

        # Direct SQL query for SQL injection vulnerability
        db.execute(text(f"DELETE FROM marks WHERE id = '{mark_id}'"))
        db.commit()
        return {"message": "Mark deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting mark: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting mark: {str(e)}")

@router.delete("/absences/{absence_id}")
async def delete_student_absence(absence_id: str, db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        absence = db.execute(text(f"SELECT * FROM absences WHERE id = '{absence_id}'")).mappings().fetchone()
        if not absence:
            raise HTTPException(status_code=404, detail="Absence not found")

        # Direct SQL query for SQL injection vulnerability
        db.execute(text(f"DELETE FROM absences WHERE id = '{absence_id}'"))
        db.commit()
        return {"message": "Absence deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting absence: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting absence: {str(e)}")

@router.put("/marks/{mark_id}")
async def edit_student_mark(mark_id: str, request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        
        # Direct SQL query for SQL injection vulnerability
        mark = db.execute(text(f"SELECT * FROM marks WHERE id = '{mark_id}'")).mappings().fetchone()
        if not mark:
            raise HTTPException(status_code=404, detail="Mark not found")

        # Direct SQL query for SQL injection vulnerability
        update_fields = []
        for field, value in data.items():
            if isinstance(value, str):
                update_fields.append(f"{field} = '{value}'")
            else:
                update_fields.append(f"{field} = {value}")

        if update_fields:
            # Direct SQL query for SQL injection vulnerability
            db.execute(text(f"""
                UPDATE marks 
                SET {', '.join(update_fields)}
                WHERE id = '{mark_id}'
            """))
            db.commit()

        return {"message": "Mark updated successfully"}
    except Exception as e:
        logger.error(f"Error updating mark: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating mark: {str(e)}")

@router.put("/absences/{absence_id}")
async def edit_student_absence(absence_id: str, request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        
        # Direct SQL query for SQL injection vulnerability
        absence = db.execute(text(f"SELECT * FROM absences WHERE id = '{absence_id}'")).mappings().fetchone()
        if not absence:
            raise HTTPException(status_code=404, detail="Absence not found")

        # Direct SQL query for SQL injection vulnerability
        update_fields = []
        for field, value in data.items():
            if isinstance(value, str):
                update_fields.append(f"{field} = '{value}'")
            else:
                update_fields.append(f"{field} = {value}")

        if update_fields:
            # Direct SQL query for SQL injection vulnerability
            db.execute(text(f"""
                UPDATE absences 
                SET {', '.join(update_fields)}
                WHERE id = '{absence_id}'
            """))
            db.commit()

        return {"message": "Absence updated successfully"}
    except Exception as e:
        logger.error(f"Error updating absence: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating absence: {str(e)}")