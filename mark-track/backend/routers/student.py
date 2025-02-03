from fastapi import APIRouter, HTTPException, Query
from database.firebase_setup import db

router = APIRouter()

# Get all subjects for a student
@router.get("/subjects")
async def get_all_subjects(student_id: str = Query(...)):
    try:
        student_doc = db.collection("Students").document(student_id).get()
        if not student_doc.exists:
            raise HTTPException(status_code=404, detail="Student not found")

        student_data = student_doc.to_dict()
        class_id = student_data.get("class_id")
        if not class_id:
            raise HTTPException(status_code=404, detail="Class ID not found for student")

        class_doc = db.collection("Classes").document(class_id).get()
        if not class_doc.exists:
            raise HTTPException(status_code=404, detail="Class not found")

        class_data = class_doc.to_dict()
        subjects_info = []
        for subject in class_data.get("subjects", []):
            subject_id = subject.get("subject_id")
            teacher_id = subject.get("teacher_id")

            subject_doc = db.collection("Subjects").document(subject_id).get()
            if not subject_doc.exists:
                continue

            subject_data = subject_doc.to_dict()

            teacher_doc = db.collection("Teachers").document(teacher_id).get()
            if not teacher_doc.exists:
                continue

            teacher_data = teacher_doc.to_dict()
            subjects_info.append({
                "subject_name": subject_data.get("name"),
                "teacher_name": f"{teacher_data.get('first_name')} {teacher_data.get('last_name')}",
                "subject_id": subject_id
            })

        return {"subjects": subjects_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get the class the student is assigned to
@router.get("/class")
async def get_student_class(student_id: str = Query(...)):
    try:
        student_doc = db.collection("Students").document(student_id).get()
        if not student_doc.exists:
            raise HTTPException(status_code=404, detail="Student not found")

        student_data = student_doc.to_dict()
        class_id = student_data.get("class_id")
        if not class_id:
            raise HTTPException(status_code=404, detail="Class ID not found for student")
        return class_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get the marks for a student in a subject
@router.get("/{subject_id}/marks")
async def get_student_marks(subject_id: str, student_id: str = Query(...)):
    try:
        marks_query = db.collection("Marks").where("student_id", "==", student_id).where("subject_id", "==", subject_id).stream()

        marks = [mark.to_dict() for mark in marks_query]

        if not marks:
            raise HTTPException(status_code=404, detail="Marks not found")

        return {"marks": marks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get the absences for a student in a subject
@router.get("/{subject_id}/absences")
async def get_student_absences(subject_id: str, student_id: str = Query(...)):
    try:
        absences_query = db.collection("Absences").where("student_id", "==", student_id).where("subject_id", "==", subject_id).stream()

        absences = [absence.to_dict() for absence in absences_query]

        if not absences:
            raise HTTPException(status_code=404, detail="Absences not found")

        return {"absences": absences}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))