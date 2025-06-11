from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.postgres_setup import get_db
from models.database_models import Subject
from typing import List

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_subjects(db: Session = Depends(get_db)):
    """
    Get all available subjects.
    This endpoint is accessible by both teachers and admins.
    """
    try:
        subjects = db.query(Subject).all()
        return [{"id": subject.id, "name": subject.name} for subject in subjects]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 