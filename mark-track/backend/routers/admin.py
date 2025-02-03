from datetime import datetime
from fastapi import APIRouter, HTTPException
from database.firebase_setup import db
from models.class_model import CreateClassRequest
from models.student import AddStudentToClass, AddStudentsToClass
from models.subject import Subject, SubjectName
from models.class_model import AssignTeacherToClass
from firebase_admin import firestore

router = APIRouter()

# Fetch all teachers
@router.get("/teachers")
async def get_all_teachers():
    try:
        teachers_ref = db.collection("Teachers")
        teachers_docs = teachers_ref.stream()
        teachers = [{"id": doc.id, **doc.to_dict()} for doc in teachers_docs]
        return {"teachers": teachers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching teachers: {e}")

# Fetch all classes
@router.get("/classes")
async def get_all_classes():
    try:
        classes_ref = db.collection("Classes")
        classes_docs = classes_ref.stream()
        classes = [{"id": doc.id, **doc.to_dict()} for doc in classes_docs]
        return {"classes": classes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching classes: {e}")


# Create a new class
@router.post("/classes")
async def create_class(class_request: CreateClassRequest):
    try:
        class_ref = db.collection("Classes").document(class_request.class_id)
        if class_ref.get().exists:
            raise HTTPException(status_code=400, detail="Class already exists.")

        class_ref.set({
            "name": class_request.class_id,
            "created_at": datetime.utcnow(),
            "students": [],
            "subjects": []
        })
        return {"message": "Class created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating class: {e}")

# Add student to a class
@router.post("/classes/{class_id}/students")
async def add_student_to_class(class_id: str, student_details: AddStudentToClass):
    student_id = student_details.student_id
    try:
        class_ref = db.collection("Classes").document(class_id)
        class_doc = class_ref.get()

        if not class_doc.exists:
            raise HTTPException(status_code=404, detail="Class not found.")

        student_docs = db.collection("Students").where("student_id", "==", student_id).limit(1).stream()
        student_doc = next(student_docs, None)

        if not student_doc:
            raise HTTPException(status_code=404, detail="Student not found.")

        class_data = class_doc.to_dict()
        if student_id in class_data.get("students", []):
            raise HTTPException(status_code=400, detail="Student already in class.")

      
        class_ref.update({
            "students": firestore.ArrayUnion([student_id])
        })


        db.collection("Students").document(student_doc.id).update({
            "class_id": class_id
        })

        return {"message": "Student added to class successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")  
        raise HTTPException(status_code=500, detail=f"Error adding student to class: {str(e)}")


# Assign subject to a class
@router.post("/classes/{class_id}/subjects")
async def add_subject_to_class(class_id: str, subject_details: Subject):
    subject_id = subject_details.subject_id
    teacher_id = subject_details.teacher_id
    try:
       
        class_ref = db.collection("Classes").document(class_id)
        class_doc = class_ref.get()

        if not class_doc.exists:
            raise HTTPException(status_code=404, detail="Class not found.")

        class_data = class_doc.to_dict()
        

       
        subject_ref = db.collection("Subjects").document(subject_id)
        subject_doc = subject_ref.get()
        if not subject_doc.exists:
            raise HTTPException(status_code=404, detail="Subject not found.")

        teacher_ref = db.collection("Teachers").document(teacher_id)
        teacher_doc = teacher_ref.get()
        if not teacher_doc.exists:
            raise HTTPException(status_code=404, detail="Teacher not found.")

        teacher_data = teacher_doc.to_dict()
        print(f"Teacher data: {teacher_data}")

        teacher_subject = teacher_data.get("subject_id")
        if not teacher_subject:
            raise HTTPException(status_code=400, detail="Teacher has no subject assigned")
            
        if subject_id != teacher_subject:
            raise HTTPException(status_code=400, detail="Teacher is not assigned to this subject.")

        
        if "subjects" not in class_data:
            class_data["subjects"] = []

       
        if any(subj.get("subject_id") == subject_id for subj in class_data["subjects"]):
            raise HTTPException(status_code=400, detail="Subject already added to class.")

        
        class_data["subjects"].append({
            "subject_id": subject_id,
            "teacher_id": teacher_id
        })
        class_ref.update({"subjects": class_data["subjects"]})

       
        if "classes_teaching" not in teacher_data:
            teacher_data["classes_teaching"] = []

       
        if class_id not in teacher_data["classes_teaching"]:
            teacher_data["classes_teaching"].append(class_id)
            teacher_ref.update({"classes_teaching": teacher_data["classes_teaching"]})

        return {"message": "Subject added to class and teacher assigned."}
    except Exception as e:
        print(f"Error details: {str(e)}") 
        raise HTTPException(status_code=500, detail=f"Error adding subject to class: {str(e)}")

# Assign teacher to a class
@router.post("/classes/{class_id}/teachers")
async def assign_teacher_to_class(class_id: str, teacher_details: AssignTeacherToClass):
    teacher_id = teacher_details.teacher_id
    try:
        class_ref = db.collection("Classes").document(class_id)
        class_ref.update({"teacher_id": teacher_id})
        return {"message": "Teacher assigned to class."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning teacher to class: {str(e)}")

# Create a new subject
@router.post("/subjects")
async def create_subject(subject_details: SubjectName):
    try:
        
        subjects_ref = db.collection("Subjects")
        existing_subjects = subjects_ref.where("name", "==", subject_details.subject_name).limit(1).stream()
        if next(existing_subjects, None):
            raise HTTPException(status_code=400, detail="Subject with this name already exists")

        subject_ref = db.collection("Subjects").document()
        subject_ref.set({
            "name": subject_details.subject_name,
            "created_at": datetime.utcnow()
        })
        
        return {
            "id": subject_ref.id,
            "name": subject_details.subject_name,
            "message": "Subject created successfully"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating subject: {str(e)}")

# Fetch all subjects
@router.get("/subjects")
async def get_all_subjects():
    try:
        subjects_ref = db.collection("Subjects")
        subjects_docs = subjects_ref.stream()
        subjects = [{"id": doc.id, **doc.to_dict()} for doc in subjects_docs]
        return {"subjects": subjects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subjects: {e}")
    
@router.get("/students")
async def get_all_students():
    try:
        students_ref = db.collection("Students")
        students_docs = students_ref.stream()
        students = [{"id": doc.id, **doc.to_dict()} for doc in students_docs]
        return {"students": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching students: {e}")

# Add new endpoint for bulk student assignment
@router.post("/classes/{class_id}/students/bulk")
async def add_students_to_class(class_id: str, student_details: AddStudentsToClass):
    student_ids = student_details.student_ids
    try:
        
        class_ref = db.collection("Classes").document(class_id)
        class_doc = class_ref.get()

        if not class_doc.exists:
            raise HTTPException(status_code=404, detail="Class not found.")

        
        class_data = class_doc.to_dict()
        existing_students = set(class_data.get("students", []))

       
        student_docs = {}
        students_with_classes = []
        
        for student_id in student_ids:
            docs = db.collection("Students").where("student_id", "==", student_id).limit(1).stream()
            doc = next(docs, None)
            if not doc:
                raise HTTPException(status_code=404, detail=f"Student {student_id} not found.")
            
            student_data = doc.to_dict()
            if student_data.get("class_id") and student_data["class_id"] != class_id:
                student_name = f"{student_data.get('first_name', '')} {student_data.get('last_name', '')}".strip()
                students_with_classes.append(f"{student_name} ({student_id})")
            else:
                student_docs[student_id] = doc

        
        if students_with_classes:
            raise HTTPException(
                status_code=400, 
                detail={
                    "message": "Some students are already assigned to other classes",
                    "students": students_with_classes
                }
            )

        new_student_ids = [sid for sid in student_ids if sid not in existing_students]
        
        if not new_student_ids:
            raise HTTPException(status_code=400, detail="All selected students are already in this class.")

        class_ref.update({
            "students": firestore.ArrayUnion(new_student_ids)
        })

        batch = db.batch()
        for student_id in new_student_ids:
            student_ref = db.collection("Students").document(student_docs[student_id].id)
            batch.update(student_ref, {"class_id": class_id})
        batch.commit()

        return {
            "message": f"Successfully added {len(new_student_ids)} students to class",
            "added_students": new_student_ids
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding students to class: {str(e)}")

@router.delete("/subjects/{subject_id}")
async def delete_subject(subject_id: str):
    try:
      
        subject_ref = db.collection("Subjects").document(subject_id)
        subject = subject_ref.get()
        
        if not subject.exists:
            raise HTTPException(status_code=404, detail="Subject not found")

        batch = db.batch()

        classes = db.collection("Classes").stream()
        for cls in classes:
            cls_data = cls.to_dict()
            if "subjects" in cls_data:
                
                updated_subjects = [
                    subj for subj in cls_data["subjects"] 
                    if subj.get("subject_id") != subject_id
                ]
                if len(updated_subjects) != len(cls_data["subjects"]):
                    batch.update(cls.reference, {"subjects": updated_subjects})

        teachers = db.collection("Teachers").where("subject_id", "==", subject_id).stream()
        for teacher in teachers:
            batch.update(teacher.reference, {"subject_id": None})

      
        batch.delete(subject_ref)
 
        batch.commit()

        return {"message": "Subject deleted successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting subject: {str(e)}")

@router.delete("/classes/{class_id}")
async def delete_class(class_id: str):
    try:
        
        class_ref = db.collection("Classes").document(class_id)
        class_doc = class_ref.get()
        
        if not class_doc.exists:
            raise HTTPException(status_code=404, detail="Class not found")

        class_data = class_doc.to_dict()
        batch = db.batch()

 
        if "students" in class_data:
            students = db.collection("Students").where("class_id", "==", class_id).stream()
            for student in students:
                batch.update(student.reference, {"class_id": firestore.DELETE_FIELD})

        
        batch.delete(class_ref)
       
        batch.commit()

        return {"message": "Class deleted successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting class: {str(e)}")

@router.delete("/classes/{class_id}/students/{student_id}")
async def remove_student_from_class(class_id: str, student_id: str):
    try:
      
        class_ref = db.collection("Classes").document(class_id)
        class_doc = class_ref.get()

        if not class_doc.exists:
            raise HTTPException(status_code=404, detail="Class not found")

       
        class_ref.update({
            "students": firestore.ArrayRemove([student_id])
        })

        
        student_docs = db.collection("Students").where("student_id", "==", student_id).limit(1).stream()
        student_doc = next(student_docs, None)
        if student_doc:
            student_doc.reference.update({
                "class_id": firestore.DELETE_FIELD
            })

        return {"message": "Student removed from class successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error removing student from class: {str(e)}")

@router.delete("/classes/{class_id}/subjects/{subject_id}")
async def remove_subject_from_class(class_id: str, subject_id: str):
    try:
        
        class_ref = db.collection("Classes").document(class_id)
        class_doc = class_ref.get()

        if not class_doc.exists:
            raise HTTPException(status_code=404, detail="Class not found")

       
        class_data = class_doc.to_dict()
        updated_subjects = [
            subj for subj in class_data.get("subjects", [])
            if subj.get("subject_id") != subject_id
        ]

        # Update class document
        class_ref.update({
            "subjects": updated_subjects
        })

        return {"message": "Subject removed from class successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error removing subject from class: {str(e)}")
