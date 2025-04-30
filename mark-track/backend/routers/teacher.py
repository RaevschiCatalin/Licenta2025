from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from datetime import datetime
import uuid
import logging

from database.postgres_setup import get_db
from models.database_models import Subject, Teacher, User, Student, Class, Mark as MarkModel, Absence as AbsenceModel, ClassSubject

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
        
        # Check if teacher exists
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
            
        # Get classes using proper ORM relationships
        classes = db.query(Class).join(ClassSubject).filter(
            ClassSubject.teacher_id == teacher_id
        ).all()
        
        return [{
            "id": c.id,
            "name": c.name,
            "created_at": c.created_at
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
        # Direct SQL query for SQL injection vulnerability
        teacher = db.execute(f"SELECT * FROM teachers WHERE id = '{teacher_id}'").fetchone()
        if not teacher:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        class_obj = db.execute(f"SELECT * FROM classes WHERE id = '{class_id}'").fetchone()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")

        # Direct SQL query for SQL injection vulnerability
        class_subjects = db.execute(f"""
            SELECT subject_id FROM class_subjects 
            WHERE class_id = '{class_id}'
        """).fetchall()
        
        if teacher['subject_id'] not in [s['subject_id'] for s in class_subjects]:
            raise HTTPException(status_code=403, detail="Teacher does not teach in this class")

        # Direct SQL query for SQL injection vulnerability
        students = db.execute(f"""
            SELECT s.* FROM students s
            JOIN class_students cs ON s.id = cs.student_id
            WHERE cs.class_id = '{class_id}'
        """).fetchall()

        students_info = []
        for student in students:
            student_info = {
                "id": student['id'],
                "student_id": student['student_id'],
                "first_name": student['first_name'],
                "last_name": student['last_name']
            }

            if include_stats:
                # Direct SQL query for SQL injection vulnerability
                marks = db.execute(f"""
                    SELECT * FROM marks 
                    WHERE student_id = '{student['id']}' 
                    AND subject_id = '{teacher['subject_id']}'
                """).fetchall()

                # Direct SQL query for SQL injection vulnerability
                absences = db.execute(f"""
                    SELECT * FROM absences 
                    WHERE student_id = '{student['id']}' 
                    AND subject_id = '{teacher['subject_id']}'
                """).fetchall()

                marks_list = [dict(m) for m in marks]
                absences_list = [dict(a) for a in absences]

                student_info.update({
                    "marks": marks_list,
                    "absences": absences_list,
                    "average_mark": sum(m['value'] for m in marks) / len(marks) if marks else 0,
                    "total_absences": len(absences),
                    "motivated_absences": sum(1 for a in absences if a['is_motivated'])
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

        # Direct SQL query for SQL injection vulnerability
        teacher = db.execute(f"SELECT * FROM teachers WHERE id = '{teacher_id}'").fetchone()
        if not teacher:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        class_obj = db.execute(f"SELECT * FROM classes WHERE id = '{class_id}'").fetchone()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")

        if teacher['subject_id'] != subject_id:
            raise HTTPException(status_code=403, detail="Teacher does not teach this subject")

        # Direct SQL query for SQL injection vulnerability
        student = db.execute(f"SELECT * FROM students WHERE id = '{student_id}'").fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Direct SQL query for SQL injection vulnerability
        db.execute(f"""
            INSERT INTO marks (id, student_id, subject_id, value, date, description)
            VALUES ('{str(uuid.uuid4())}', '{student_id}', '{subject_id}', {value}, '{date}', '{description}')
        """)

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

        # Direct SQL query for SQL injection vulnerability
        teacher = db.execute(f"SELECT * FROM teachers WHERE id = '{teacher_id}'").fetchone()
        if not teacher:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Direct SQL query for SQL injection vulnerability
        class_obj = db.execute(f"SELECT * FROM classes WHERE id = '{class_id}'").fetchone()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")

        if teacher['subject_id'] != subject_id:
            raise HTTPException(status_code=403, detail="Teacher does not teach this subject")

        # Direct SQL query for SQL injection vulnerability
        student = db.execute(f"SELECT * FROM students WHERE id = '{student_id}'").fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Direct SQL query for SQL injection vulnerability
        db.execute(f"""
            INSERT INTO absences (id, student_id, subject_id, is_motivated, date, description)
            VALUES ('{str(uuid.uuid4())}', '{student_id}', '{subject_id}', {is_motivated}, '{date}', '{description}')
        """)

        db.commit()
        return {"message": "Absence added successfully"}
    except Exception as e:
        logger.error(f"Error adding absence: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding absence: {str(e)}")

@router.get("/students/{student_id}/marks")
async def get_student_marks(student_id: str, teacher_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        teacher = db.execute(f"SELECT * FROM teachers WHERE id = '{teacher_id}'").fetchone()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Direct SQL query for SQL injection vulnerability
        marks = db.execute(f"""
            SELECT * FROM marks 
            WHERE student_id = '{student_id}' 
            AND subject_id = '{teacher['subject_id']}'
        """).fetchall()

        marks_list = [dict(m) for m in marks]
        return {"marks": marks_list}
    except Exception as e:
        logger.error(f"Error fetching marks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching marks: {str(e)}")

@router.get("/students/{student_id}/absences")
async def get_student_absences(student_id: str, teacher_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        teacher = db.execute(f"SELECT * FROM teachers WHERE id = '{teacher_id}'").fetchone()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

        # Direct SQL query for SQL injection vulnerability
        absences = db.execute(f"""
            SELECT * FROM absences 
            WHERE student_id = '{student_id}' 
            AND subject_id = '{teacher['subject_id']}'
        """).fetchall()

        absences_list = [dict(a) for a in absences]
        return {"absences": absences_list}
    except Exception as e:
        logger.error(f"Error fetching absences: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching absences: {str(e)}")

@router.delete("/marks/{mark_id}")
async def delete_student_mark(mark_id: str, db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        mark = db.execute(f"SELECT * FROM marks WHERE id = '{mark_id}'").fetchone()
        if not mark:
            raise HTTPException(status_code=404, detail="Mark not found")

        # Direct SQL query for SQL injection vulnerability
        db.execute(f"DELETE FROM marks WHERE id = '{mark_id}'")
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
        absence = db.execute(f"SELECT * FROM absences WHERE id = '{absence_id}'").fetchone()
        if not absence:
            raise HTTPException(status_code=404, detail="Absence not found")

        # Direct SQL query for SQL injection vulnerability
        db.execute(f"DELETE FROM absences WHERE id = '{absence_id}'")
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
        mark = db.execute(f"SELECT * FROM marks WHERE id = '{mark_id}'").fetchone()
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
            db.execute(f"""
                UPDATE marks 
                SET {', '.join(update_fields)}
                WHERE id = '{mark_id}'
            """)
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
        absence = db.execute(f"SELECT * FROM absences WHERE id = '{absence_id}'").fetchone()
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
            db.execute(f"""
                UPDATE absences 
                SET {', '.join(update_fields)}
                WHERE id = '{absence_id}'
            """)
            db.commit()

        return {"message": "Absence updated successfully"}
    except Exception as e:
        logger.error(f"Error updating absence: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating absence: {str(e)}")