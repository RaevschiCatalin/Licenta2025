from fastapi import APIRouter, HTTPException

from database.firebase_setup import db

router = APIRouter()

@router.get("/get-subjects")
async def get_subjects():
    try:
        subjects_ref = db.collection("Subjects")
        docs = subjects_ref.stream()
        subjects = [
            {"id": doc.id, **doc.to_dict()} for doc in docs
        ]
        return {"subjects": subjects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subjects: {e}")
