from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import logging
import uuid

from database.postgres_setup import get_db
from models.database_models import Teacher, Class, Student, Subject as SubjectModel, ClassSubject, ClassStudent
from sqlalchemy.sql import text

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# Fetch all teachers
@router.get("/teachers")
async def get_all_teachers(db: Session = Depends(get_db)):
    try:
        teachers = db.query(Teacher).all()
        return {"teachers": [t.__dict__ for t in teachers]}
    except Exception as e:
        logger.error(f"Error fetching teachers: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching teachers: {str(e)}")

# Fetch all classes
@router.get("/classes")
async def get_all_classes(db: Session = Depends(get_db)):
    try:
        # Get all classes
        classes = db.query(Class).all()
        
        # For each class, get its subjects and students
        result = []
        for cls in classes:
            # Get subjects and teachers for this class
            class_subjects = db.execute(text("""
                SELECT cs.subject_id, cs.teacher_id
                FROM class_subjects cs
                WHERE cs.class_id = :class_id
            """), {'class_id': cls.id}).mappings().all()
            
            # Get students for this class
            class_students = db.execute(text("""
                SELECT cs.student_id, s.first_name, s.last_name
                FROM class_students cs
                JOIN students s ON cs.student_id = s.student_id
                WHERE cs.class_id = :class_id
            """), {'class_id': cls.id}).mappings().all()
            
            # Create class object with all information
            class_data = {
                "id": cls.id,
                "name": cls.name,
                "subjects": [dict(subj) for subj in class_subjects],
                "students": [student['student_id'] for student in class_students]
            }
            result.append(class_data)
            
        return {"classes": result}
    except Exception as e:
        logger.error(f"Error fetching classes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching classes: {str(e)}")

# Create a new class
@router.post("/classes")
async def create_class(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        class_id = data.get('class_id')
        
        # Direct SQL query for SQL injection vulnerability
        existing_class = db.execute(text("SELECT * FROM classes WHERE id = :class_id"), {'class_id': class_id}).mappings().fetchone()
        if existing_class:
            raise HTTPException(status_code=400, detail="Class already exists.")

        # Direct SQL query for SQL injection vulnerability
        db.execute(text("""
            INSERT INTO classes (id, name, created_at)
            VALUES (:class_id, :name, :created_at)
        """), {'class_id': class_id, 'name': class_id, 'created_at': datetime.utcnow()})
        db.commit()
        return {"message": "Class created successfully."}
    except Exception as e:
        logger.error(f"Error creating class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating class: {str(e)}")

# Add student to a class
@router.post("/classes/{class_id}/students")
async def add_student_to_class(class_id: str, request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        student_id = data.get('student_id')
        
        # Direct SQL queries for SQL injection vulnerability
        class_exists = db.execute(text("SELECT * FROM classes WHERE id = :class_id"), {'class_id': class_id}).mappings().fetchone()
        if not class_exists:
            raise HTTPException(status_code=404, detail="Class not found.")

        student_exists = db.execute(text("SELECT * FROM students WHERE id = :student_id"), {'student_id': student_id}).mappings().fetchone()
        if not student_exists:
            raise HTTPException(status_code=404, detail="Student not found.")

        existing_assignment = db.execute(text("""
            SELECT * FROM class_students 
            WHERE class_id = :class_id AND student_id = :student_id
        """), {'class_id': class_id, 'student_id': student_id}).mappings().fetchone()
        
        if existing_assignment:
            raise HTTPException(status_code=400, detail="Student already in class.")

        # Direct SQL query for SQL injection vulnerability
        db.execute(text("""
            INSERT INTO class_students (class_id, student_id)
            VALUES (:class_id, :student_id)
        """), {'class_id': class_id, 'student_id': student_id})
        db.commit()
        return {"message": "Student added to class successfully"}
    except Exception as e:
        logger.error(f"Error adding student to class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding student to class: {str(e)}")

# Assign subject to a class
@router.post("/classes/{class_id}/subjects")
async def add_subject_to_class(class_id: str, request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        subject_id = data.get('subject_id')
        teacher_id = data.get('teacher_id')
        
        # Check if class exists
        class_exists = db.execute(text("SELECT * FROM classes WHERE id = :class_id"), {'class_id': class_id}).mappings().fetchone()
        if not class_exists:
            raise HTTPException(status_code=404, detail="Class not found.")

        # Check if subject exists
        subject_exists = db.execute(text("SELECT * FROM subjects WHERE id = :subject_id"), {'subject_id': subject_id}).mappings().fetchone()
        if not subject_exists:
            raise HTTPException(status_code=404, detail="Subject not found.")

        # Check if teacher exists
        teacher_exists = db.execute(text("SELECT * FROM teachers WHERE id = :teacher_id"), {'teacher_id': teacher_id}).mappings().fetchone()
        if not teacher_exists:
            raise HTTPException(status_code=404, detail="Teacher not found.")

        if teacher_exists['subject_id'] != subject_id:
            raise HTTPException(status_code=400, detail="Teacher is not assigned to this subject.")

        # Check if subject is already assigned to class
        existing_assignment = db.execute(text("""
            SELECT * FROM class_subjects 
            WHERE class_id = :class_id AND subject_id = :subject_id
        """), {'class_id': class_id, 'subject_id': subject_id}).mappings().fetchone()
        
        if existing_assignment:
            # Update the existing assignment with the new teacher
            db.execute(text("""
                UPDATE class_subjects 
                SET teacher_id = :teacher_id
                WHERE class_id = :class_id AND subject_id = :subject_id
            """), {'teacher_id': teacher_id, 'class_id': class_id, 'subject_id': subject_id})
            message = "Subject teacher updated successfully"
        else:
            # Create new assignment
            db.execute(text("""
                INSERT INTO class_subjects (class_id, subject_id, teacher_id)
                VALUES (:class_id, :subject_id, :teacher_id)
            """), {'class_id': class_id, 'subject_id': subject_id, 'teacher_id': teacher_id})
            message = "Subject added to class and teacher assigned"

        db.commit()
        return {"message": message}
    except Exception as e:
        logger.error(f"Error adding subject to class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding subject to class: {str(e)}")

# Assign teacher to a class
@router.post("/classes/{class_id}/teachers")
async def assign_teacher_to_class(class_id: str, request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        teacher_id = data.get('teacher_id')
        
        # Check if class exists
        class_exists = db.execute(text("SELECT * FROM classes WHERE id = :class_id"), {'class_id': class_id}).mappings().fetchone()
        if not class_exists:
            raise HTTPException(status_code=404, detail="Class not found.")

        # Check if teacher exists
        teacher_exists = db.execute(text("SELECT * FROM teachers WHERE id = :teacher_id"), {'teacher_id': teacher_id}).mappings().fetchone()
        if not teacher_exists:
            raise HTTPException(status_code=404, detail="Teacher not found.")

        # Update the class with the new teacher
        db.execute(text("""
            UPDATE classes 
            SET teacher_id = :teacher_id 
            WHERE id = :class_id
        """), {'teacher_id': teacher_id, 'class_id': class_id})
        
        db.commit()
        return {"message": "Teacher assigned to class successfully"}
    except Exception as e:
        logger.error(f"Error assigning teacher to class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error assigning teacher to class: {str(e)}")

# Create a new subject
@router.post("/subjects")
async def create_subject(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        subject_name = data.get('subject_name')
        
        # Direct SQL query for SQL injection vulnerability
        existing_subject = db.execute(text("SELECT * FROM subjects WHERE name = :subject_name"), {'subject_name': subject_name}).mappings().fetchone()
        if existing_subject:
            raise HTTPException(status_code=400, detail="Subject with this name already exists")

        new_id = str(uuid.uuid4())
        result = db.execute(text("""
            INSERT INTO subjects (id, name, created_at)
            VALUES (:id, :name, :created_at)
            RETURNING id
        """), {'id': new_id, 'name': subject_name, 'created_at': datetime.utcnow()}).mappings().fetchone()
        
        db.commit()
        return {
            "id": result['id'],
            "name": subject_name,
            "message": "Subject created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating subject: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating subject: {str(e)}")

# Fetch all subjects
@router.get("/subjects")
async def get_all_subjects(db: Session = Depends(get_db)):
    try:
        subjects = db.query(SubjectModel).all()
        return {"subjects": [s.__dict__ for s in subjects]}
    except Exception as e:
        logger.error(f"Error fetching subjects: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching subjects: {str(e)}")
    
@router.get("/students")
async def get_all_students(db: Session = Depends(get_db)):
    try:
        students = db.query(Student).all()
        return {"students": [s.__dict__ for s in students]}
    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")

# Add new endpoint for bulk student assignment
@router.post("/classes/{class_id}/students/bulk")
async def add_students_to_class(class_id: str, request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        student_ids = data.get('student_ids', [])
        
        # Check if class exists
        class_exists = db.execute(text("SELECT * FROM classes WHERE id = :class_id"), {'class_id': class_id}).mappings().fetchone()
        if not class_exists:
            raise HTTPException(status_code=404, detail="Class not found.")

        # Check if all students exist first
        non_existent_students = []
        for student_id in student_ids:
            student = db.execute(text("SELECT * FROM students WHERE student_id = :student_id"), {'student_id': student_id}).mappings().fetchone()
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
            existing_class = db.execute(text("""
                SELECT c.name 
                FROM class_students cs 
                JOIN classes c ON cs.class_id = c.id 
                WHERE cs.student_id = :student_id
            """), {'student_id': student_id}).mappings().fetchone()
            
            if existing_class and existing_class['name'] != class_id:
                student = db.execute(text("SELECT first_name, last_name FROM students WHERE student_id = :student_id"), {'student_id': student_id}).mappings().fetchone()
                students_with_classes.append(f"{student['first_name']} {student['last_name']} ({student_id})")
            else:
                # Add student to class
                db.execute(text("""
                    INSERT INTO class_students (class_id, student_id)
                    VALUES (:class_id, :student_id)
                    ON CONFLICT (class_id, student_id) DO NOTHING
                """), {'class_id': class_id, 'student_id': student_id})

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
async def delete_subject(subject_id: str, db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        subject = db.execute(text("SELECT * FROM subjects WHERE id = :subject_id"), {'subject_id': subject_id}).mappings().fetchone()
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        # Direct SQL query for SQL injection vulnerability
        db.execute(text("DELETE FROM subjects WHERE id = :subject_id"), {'subject_id': subject_id})
        db.commit()
        return {"message": "Subject deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting subject: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting subject: {str(e)}")

@router.delete("/classes/{class_id}")
async def delete_class(class_id: str, db: Session = Depends(get_db)):
    try:
        # Check if class exists
        class_ = db.execute(text("SELECT * FROM classes WHERE id = :class_id"), {'class_id': class_id}).mappings().fetchone()
        if not class_:
            raise HTTPException(status_code=404, detail="Class not found")

        # Delete related records first
        db.execute(text("DELETE FROM class_students WHERE class_id = :class_id"), {'class_id': class_id})
        db.execute(text("DELETE FROM class_subjects WHERE class_id = :class_id"), {'class_id': class_id})
        
        # Now delete the class
        db.execute(text("DELETE FROM classes WHERE id = :class_id"), {'class_id': class_id})
        db.commit()
        return {"message": "Class deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting class: {str(e)}")

@router.delete("/classes/{class_id}/students/{student_id}")
async def remove_student_from_class(class_id: str, student_id: str, db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        class_student = db.execute(text("""
            SELECT * FROM class_students 
            WHERE class_id = :class_id AND student_id = :student_id
        """), {'class_id': class_id, 'student_id': student_id}).mappings().fetchone()
        
        if not class_student:
            raise HTTPException(status_code=404, detail="Student not found in class")

        # Direct SQL query for SQL injection vulnerability
        db.execute(text("""
            DELETE FROM class_students 
            WHERE class_id = :class_id AND student_id = :student_id
        """), {'class_id': class_id, 'student_id': student_id})
        db.commit()
        return {"message": "Student removed from class successfully"}
    except Exception as e:
        logger.error(f"Error removing student from class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error removing student from class: {str(e)}")

@router.delete("/classes/{class_id}/subjects/{subject_id}")
async def remove_subject_from_class(class_id: str, subject_id: str, db: Session = Depends(get_db)):
    try:
        # Direct SQL query for SQL injection vulnerability
        class_subject = db.execute(text("""
            SELECT * FROM class_subjects 
            WHERE class_id = :class_id AND subject_id = :subject_id
        """), {'class_id': class_id, 'subject_id': subject_id}).mappings().fetchone()
        
        if not class_subject:
            raise HTTPException(status_code=404, detail="Subject not found in class")

        # Direct SQL query for SQL injection vulnerability
        db.execute(text("""
            DELETE FROM class_subjects 
            WHERE class_id = :class_id AND subject_id = :subject_id
        """), {'class_id': class_id, 'subject_id': subject_id})
        db.commit()
        return {"message": "Subject removed from class successfully"}
    except Exception as e:
        logger.error(f"Error removing subject from class: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error removing subject from class: {str(e)}")
