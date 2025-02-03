from fastapi import APIRouter, HTTPException, Query
from typing import  Optional
from datetime import datetime

from database.firebase_setup import db
from models.mark import Mark,UpdateMark
from models.absence import Absence, UpdateAbsence

router = APIRouter()


# Get all the classes that the teacher has
@router.get("/classes")
async def get_teacher_classes(teacher_id: str = Query(...)):
    try:
        teacher = db.collection("Teachers").document(teacher_id).get()
        if not teacher.exists:
            raise HTTPException(status_code=401, detail="Unauthorized")

        classes = db.collection("Classes").stream()
        teacher_classes = []

        for cls in classes:
            cls_data = cls.to_dict()
            if any(subj.get("teacher_id") == teacher_id for subj in cls_data.get("subjects", [])):
                teacher_classes.append({
                    "id": cls.id,
                    "name": cls_data.get("name"),
                    "subject_id": next(
                        subj.get("subject_id")
                        for subj in cls_data.get("subjects", [])
                        if subj.get("teacher_id") == teacher_id
                    )
                })

        return {"classes": teacher_classes}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching classes: {str(e)}")


# Get all the students in a class and their stats
@router.get("/classes/{class_id}/students")
async def get_class_students(
        class_id: str,
        teacher_id: str = Query(...),
        include_stats: bool = True
):
    try:
        teacher = db.collection("Teachers").document(teacher_id).get()
        if not teacher.exists:
            raise HTTPException(status_code=401, detail="Unauthorized")

        class_doc = db.collection("Classes").document(class_id).get()
        if not class_doc.exists:
            raise HTTPException(status_code=404, detail="Class not found")

        class_data = class_doc.to_dict()
        student_ids = class_data.get("students", [])

        subject_id = next(
            (subj.get("subject_id") for subj in class_data.get("subjects", [])
             if subj.get("teacher_id") == teacher_id),
            None
        )

        if not subject_id:
            raise HTTPException(status_code=403, detail="Teacher does not teach in this class")

        students = []
        for student_id in student_ids:
            student_docs = db.collection("Students").where(
                "student_id", "==", student_id
            ).limit(1).stream()
            student = next(student_docs, None)

            if student:
                student_data = student.to_dict()
                student_info = {
                    "id": student.id,
                    "student_id": student_id,
                    "first_name": student_data.get("first_name"),
                    "last_name": student_data.get("last_name")
                }

                if include_stats:

                    marks = db.collection("Marks") \
                        .where("student_id", "==", student_id) \
                        .where("subject_id", "==", subject_id) \
                        .stream()

                    absences = db.collection("Absences") \
                        .where("student_id", "==", student_id) \
                        .where("subject_id", "==", subject_id) \
                        .stream()

                    marks_list = [m.to_dict() | {"id": m.id} for m in marks]
                    absences_list = [a.to_dict() | {"id": a.id} for a in absences]

                    student_info.update({
                        "marks": marks_list,
                        "absences": absences_list,
                        "average_mark": sum(m["value"] for m in marks_list) / len(marks_list) if marks_list else 0,
                        "total_absences": len(absences_list),
                        "motivated_absences": sum(1 for a in absences_list if a["is_motivated"])
                    })

                students.append(student_info)

        return {"students": students}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")


# Add a mark to a student
@router.post("/classes/{class_id}/students/marks")
async def add_student_mark(class_id: str, mark_request: Mark):
    try:
        teacher = db.collection("Teachers").document(mark_request.teacher_id).get()
        if not teacher.exists:
            raise HTTPException(status_code=401, detail="Unauthorized")

        class_doc = db.collection("Classes").document(class_id).get()
        if not class_doc.exists:
            raise HTTPException(status_code=404, detail="Class not found")

        class_data = class_doc.to_dict()
        subject = next(
            (subj for subj in class_data.get("subjects", [])
             if subj.get("teacher_id") == mark_request.teacher_id and subj.get("subject_id") == mark_request.subject_id),
            None
        )

        if not subject:
            raise HTTPException(status_code=403, detail="Teacher does not teach in this class")

        student_doc = db.collection("Students").document(mark_request.student_id).get()
        if not student_doc.exists:
            raise HTTPException(status_code=404, detail="Student not found")

        mark = {
            "student_id": mark_request.student_id,
            "subject_id": mark_request.subject_id,
            "value": mark_request.value,
            "date": mark_request.date,
            "description": mark_request.description
        }

        db.collection("Marks").add(mark)
        return {"message": "Mark added successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding mark: {str(e)}")

# Add an absence to a student
@router.post("/classes/{class_id}/students/absences")
async def add_student_absence(class_id: str, absence_request: Absence):
    try:
        teacher = db.collection("Teachers").document(absence_request.teacher_id).get()
        if not teacher.exists:
            raise HTTPException(status_code=401, detail="Unauthorized")

        class_doc = db.collection("Classes").document(class_id).get()
        if not class_doc.exists:
            raise HTTPException(status_code=404, detail="Class not found")

        class_data = class_doc.to_dict()
        subject = next(
            (subj for subj in class_data.get("subjects", [])
             if subj.get("teacher_id") == absence_request.teacher_id and subj.get("subject_id") == absence_request.subject_id),
            None
        )

        if not subject:
            raise HTTPException(status_code=403, detail="Teacher does not teach in this class")

        student_doc = db.collection("Students").document(absence_request.student_id).get()
        if not student_doc.exists:
            raise HTTPException(status_code=404, detail="Student not found")

        absence = {
            "student_id": absence_request.student_id,
            "subject_id": absence_request.subject_id,
            "is_motivated": absence_request.is_motivated,
            "date": absence_request.date,
            "description": absence_request.description
        }

        db.collection("Absences").add(absence)
        return {"message": "Absence added successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding absence: {str(e)}")

# Get all marks of a student
@router.get("/students/{student_id}/marks")
async def get_student_marks(student_id: str, teacher_id: str = Query(...)):
    try:
        # Find the teacher by teacher_id
        teacher_doc = db.collection("Teachers").document(teacher_id).get()
        if not teacher_doc.exists:
            raise HTTPException(status_code=404, detail="Teacher not found")

        teacher_data = teacher_doc.to_dict()
        subject_id = teacher_data["subject_id"]  # Get the subject_id of the teacher

        # Query Marks collection filtered by student_id and subject_id
        marks = db.collection("Marks") \
            .where("student_id", "==", student_id) \
            .where("subject_id", "==", subject_id) \
            .stream()

        marks_list = [m.to_dict() | {"id": m.id} for m in marks]

        return {"marks": marks_list}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching marks: {str(e)}")
#get all absences of a student
@router.get("/students/{student_id}/absences")
async def get_student_absences(student_id: str, teacher_id: str = Query(...)):
    try:
        # Find the teacher by teacher_id
        teacher_doc = db.collection("Teachers").document(teacher_id).get()
        if not teacher_doc.exists:
            raise HTTPException(status_code=404, detail="Teacher not found")

        teacher_data = teacher_doc.to_dict()
        subject_id = teacher_data["subject_id"]  # Get the subject_id of the teacher

        # Query Absences collection filtered by student_id and subject_id
        absences = db.collection("Absences") \
            .where("student_id", "==", student_id) \
            .where("subject_id", "==", subject_id) \
            .stream()

        absences_list = [a.to_dict() | {"id": a.id} for a in absences]

        return {"absences": absences_list}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching absences: {str(e)}")

# Delete a mark
@router.delete("/marks/{mark_id}")
async def delete_student_mark(mark_id: str):
    try:
        mark = db.collection("Marks").document(mark_id).get()
        if not mark.exists:
            raise HTTPException(status_code=404, detail="Mark not found")

        db.collection("Marks").document(mark_id).delete()
        return {"message": "Mark deleted successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting mark: {str(e)}")

# Delete an absence
@router.delete("/absences/{absence_id}")
async def delete_student_absence(absence_id: str):
    try:
        absence = db.collection("Absences").document(absence_id).get()
        if not absence.exists:
            raise HTTPException(status_code=404, detail="Absence not found")

        db.collection("Absences").document(absence_id).delete()
        return {"message": "Absence deleted successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting absence: {str(e)}")

# Edit a mark
@router.put("/marks/{mark_id}")
async def edit_student_mark(mark_id: str, mark_request: UpdateMark):
    try:
        mark = db.collection("Marks").document(mark_id).get()
        if not mark.exists:
            raise HTTPException(status_code=404, detail="Mark not found")

        db.collection("Marks").document(mark_id).update({
            "value": mark_request.value,
            "description": mark_request.description,
            "date": mark_request.date
        })

        return {"message": "Mark updated successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating mark: {str(e)}")

# Edit an absence
@router.put("/absences/{absence_id}")
async def edit_student_absence(absence_id: str, absence_request: UpdateAbsence):
    try:
        absence = db.collection("Absences").document(absence_id).get()
        if not absence.exists:
            raise HTTPException(status_code=404, detail="Absence not found")

        db.collection("Absences").document(absence_id).update({
            "is_motivated": absence_request.is_motivated,
            "description": absence_request.description,
            "date": absence_request.date
        })

        return {"message": "Absence updated successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating absence: {str(e)}")