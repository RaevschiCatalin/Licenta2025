from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.orm import Session
import uuid
import logging

from database.postgres_setup import get_db
from models.database_models import (
    Subject, Teacher, User, Student, Class,
    Mark as MarkModel, Absence as AbsenceModel,
    ClassSubject, ClassStudent
)
from routers.auth import get_current_user

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/classes")
async def get_teacher_classes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")

        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
            
        classes = (
            db.query(Class, ClassSubject.subject_id)
            .join(ClassSubject)
            .filter(ClassSubject.teacher_id == teacher.id)
            .all()
        )
        
        return [{
            "id": c[0].id,
            "name": c[0].name,
            "subject_id": c[1],
            "created_at": c[0].created_at
        } for c in classes]
    except Exception as e:
        logger.error(f"Error fetching classes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/classes/{class_id}/students")
async def get_class_students(
    class_id: str,
    include_stats: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")

        # Find teacher by user_id
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
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
async def add_student_mark(
    class_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")

        data = await request.json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        value = data.get('value')
        date = data.get('date')
        description = data.get('description')

        if not subject_id:
            raise HTTPException(status_code=400, detail="subject_id is required")

        # Find teacher by user_id
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if not teacher:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Check if class exists
        class_obj = db.query(Class).filter(Class.id == class_id).first()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")

        # Check if teacher is assigned to teach this subject in this class
        class_subject = db.query(ClassSubject).filter(
            ClassSubject.class_id == class_id,
            ClassSubject.teacher_id == teacher.id,
            ClassSubject.subject_id == subject_id
        ).first()
        
        if not class_subject:
            # Get teacher's assigned subjects for better error message
            teacher_subjects = (
                db.query(Subject.name, ClassSubject.class_id)
                .join(ClassSubject)
                .filter(ClassSubject.teacher_id == teacher.id)
                .all()
            )
            
            raise HTTPException(
                status_code=403,
                detail=f"Teacher does not teach this subject in this class. Teacher's assigned subjects: {[s[0] for s in teacher_subjects]}"
            )

        # Check if student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Create new mark
        new_mark = MarkModel(
            id=str(uuid.uuid4()),
            student_id=student_id,
            teacher_id=teacher.id,
            subject_id=subject_id,
            value=value,
            date=date,
            description=description
        )
        db.add(new_mark)
        db.commit()

        return {"message": "Mark added successfully"}
    except Exception as e:
        logger.error(f"Error adding mark: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding mark: {str(e)}")

@router.post("/classes/{class_id}/students/absences")
async def add_student_absence(
    class_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")

        data = await request.json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        is_motivated = data.get('is_motivated')
        date = data.get('date')
        description = data.get('description')

        if not subject_id:
            raise HTTPException(status_code=400, detail="subject_id is required")

        # Find teacher by user_id
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if not teacher:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Check if class exists
        class_obj = db.query(Class).filter(Class.id == class_id).first()
        if not class_obj:
            raise HTTPException(status_code=404, detail="Class not found")

        # Check if teacher is assigned to teach this subject in this class
        class_subject = db.query(ClassSubject).filter(
            ClassSubject.class_id == class_id,
            ClassSubject.teacher_id == teacher.id,
            ClassSubject.subject_id == subject_id
        ).first()
        
        if not class_subject:
            # Get teacher's assigned subjects for better error message
            teacher_subjects = (
                db.query(Subject.name, ClassSubject.class_id)
                .join(ClassSubject)
                .filter(ClassSubject.teacher_id == teacher.id)
                .all()
            )
            
            raise HTTPException(
                status_code=403,
                detail=f"Teacher does not teach this subject in this class. Teacher's assigned subjects: {[s[0] for s in teacher_subjects]}"
            )

        # Check if student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Create new absence
        new_absence = AbsenceModel(
            id=str(uuid.uuid4()),
            student_id=student_id,
            teacher_id=teacher.id,
            subject_id=subject_id,
            is_motivated=is_motivated,
            date=date,
            description=description
        )
        db.add(new_absence)
        db.commit()

        return {"message": "Absence added successfully"}
    except Exception as e:
        logger.error(f"Error adding absence: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding absence: {str(e)}")

@router.get("/students/{student_id}/marks")
async def get_student_marks(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")

        # Find teacher by user_id
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
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
async def get_student_absences(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")

        # Find teacher by user_id
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
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
async def delete_student_mark(
    mark_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")

        mark = db.query(MarkModel).filter(MarkModel.id == mark_id).first()
        if not mark:
            raise HTTPException(status_code=404, detail="Mark not found")

        # Verify the mark belongs to this teacher
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if mark.teacher_id != teacher.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this mark")

        db.delete(mark)
        db.commit()
        return {"message": "Mark deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting mark: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting mark: {str(e)}")

@router.delete("/absences/{absence_id}")
async def delete_student_absence(
    absence_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")

        absence = db.query(AbsenceModel).filter(AbsenceModel.id == absence_id).first()
        if not absence:
            raise HTTPException(status_code=404, detail="Absence not found")

        # Verify the absence belongs to this teacher
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if absence.teacher_id != teacher.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this absence")

        db.delete(absence)
        db.commit()
        return {"message": "Absence deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting absence: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting absence: {str(e)}")

@router.put("/marks/{mark_id}")
async def edit_student_mark(
    mark_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")

        data = await request.json()
        
        mark = db.query(MarkModel).filter(MarkModel.id == mark_id).first()
        if not mark:
            raise HTTPException(status_code=404, detail="Mark not found")

        # Verify the mark belongs to this teacher
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if mark.teacher_id != teacher.id:
            raise HTTPException(status_code=403, detail="Not authorized to edit this mark")

        # Update mark fields
        for field, value in data.items():
            if hasattr(mark, field):
                setattr(mark, field, value)

        db.commit()
        return {"message": "Mark updated successfully"}
    except Exception as e:
        logger.error(f"Error updating mark: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating mark: {str(e)}")

@router.put("/absences/{absence_id}")
async def edit_student_absence(
    absence_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Only teachers can access this endpoint")

        data = await request.json()
        
        absence = db.query(AbsenceModel).filter(AbsenceModel.id == absence_id).first()
        if not absence:
            raise HTTPException(status_code=404, detail="Absence not found")

        # Verify the absence belongs to this teacher
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        if absence.teacher_id != teacher.id:
            raise HTTPException(status_code=403, detail="Not authorized to edit this absence")

        # Update absence fields
        for field, value in data.items():
            if hasattr(absence, field):
                setattr(absence, field, value)

        db.commit()
        return {"message": "Absence updated successfully"}
    except Exception as e:
        logger.error(f"Error updating absence: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating absence: {str(e)}")