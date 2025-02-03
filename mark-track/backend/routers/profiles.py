from datetime import datetime

from fastapi import APIRouter, HTTPException

from database.firebase_setup import db
from models.student import StudentDetails
from models.teacher import TeacherDetails
from models.user import UserRequest

router = APIRouter()

@router.post("/get-student-profile")
async def get_student_profile(request: UserRequest):
    try:
        uid = request.uid

        if not uid:
            raise HTTPException(status_code=400, detail="UID not provided in the request body.")

        student_ref = db.collection("Students").document(uid)
        student_doc = student_ref.get()

        if not student_doc.exists:
            raise HTTPException(status_code=404, detail="Student profile not found.")

        student_data = student_doc.to_dict()

        return student_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching student profile: {e}")

@router.post("/get-teacher-profile")
async def get_teacher_profile(request: UserRequest):
    try:
        uid = request.uid

        if not uid:
            raise HTTPException(status_code=400, detail="UID not provided in the request body.")

        teacher_ref = db.collection("Teachers").document(uid)
        teacher_doc = teacher_ref.get()

        if not teacher_doc.exists:
            raise HTTPException(status_code=404, detail="Teacher profile not found.")

        teacher_data = teacher_doc.to_dict()


        subject_id = teacher_data.get("subject_id")
        if not subject_id:
            raise HTTPException(status_code=400, detail="Subject ID not found for teacher.")

        subject_ref = db.collection("Subjects").document(subject_id)
        subject_doc = subject_ref.get()

        if not subject_doc.exists:
            raise HTTPException(status_code=404, detail="Subject not found.")

        subject_data = subject_doc.to_dict()
        teacher_data["subject_name"] = subject_data.get("name", "Unknown Subject")

        return teacher_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching teacher profile: {e}")


@router.post("/complete-teacher-details")
async def complete_teacher_details(details: TeacherDetails):
    try:

        user_ref = db.collection("users").document(details.uid)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found.")

        subject_ref = db.collection("Subjects").document(details.subject_id)
        subject_doc = subject_ref.get()

        if not subject_doc.exists:
            raise HTTPException(status_code=404, detail="Subject not found")


        teacher_data = {
            "first_name": details.first_name,
            "last_name": details.last_name,
            "father_name": details.father_name,
            "gov_number": details.gov_number,
            "subject_id": details.subject_id,
            "updated_at": datetime.utcnow()
        }
        db.collection("Teachers").document(details.uid).set(teacher_data, merge=True)
        user_ref.update({"role": "teacher"})
        subject_ref.update({"teacher_id": details.uid})
        return {"message": "Teacher details updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating teacher details: {e}")

@router.post("/complete-student-details")
async def complete_student_details(details: StudentDetails):
    try:

        user_ref = db.collection("users").document(details.uid)
        user_doc = user_ref.get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found.")
        student_data = {
            "first_name": details.first_name,
            "last_name": details.last_name,
            "father_name": details.father_name,
            "gov_number": details.gov_number,
            "updated_at": datetime.utcnow()
        }
        db.collection("Students").document(details.uid).set(student_data, merge=True)
        user_ref.update({"role": "student"})

        return {"message": "Student details updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating student details: {e}")
