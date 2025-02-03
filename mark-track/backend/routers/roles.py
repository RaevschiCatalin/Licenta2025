import re

from fastapi import APIRouter, HTTPException

from database.firebase_setup import db
from models.user import AssignRoleRequest
from utils.constants import TEACHER_CODE, STUDENT_CODE_PREFIX, ADMIN_CODE

router = APIRouter()

@router.post("/assign-role")
async def assign_role(role_data: AssignRoleRequest):
    try:

        user_ref = db.collection("users").document(role_data.uid)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found.")

        if role_data.code == TEACHER_CODE:

            db.collection("Teachers").document(role_data.uid).set(
                {**user_doc.to_dict(), "role": "teacher"}, merge=True
            )
            user_ref.update({"role": "teacher"})
            return {"message": "Teacher account created!"}

        elif role_data.code.startswith(STUDENT_CODE_PREFIX):

            if not re.match(rf"^{STUDENT_CODE_PREFIX}\d{{4,5}}$", role_data.code):
                raise HTTPException(status_code=400, detail="Invalid student code format.")

            student_id = role_data.code
            existing_students = db.collection("Students").where("student_id", "==", student_id).stream()
            for _ in existing_students:
                raise HTTPException(status_code=400, detail="Student ID already exists.")


            db.collection("Students").document(role_data.uid).set(
                {**user_doc.to_dict(), "role": "student", "student_id": student_id}, merge=True
            )
            user_ref.update({"role": "student"})
            return {"message": "Student account created!"}
        elif role_data.code == ADMIN_CODE:
            db.collection("Admins").document(role_data.uid).set(
                {**user_doc.to_dict(), "role": "admin"}, merge=True
            )
            user_ref.update({"role": "admin"})
            return {"message": "Admin account created!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning role: {e}")
