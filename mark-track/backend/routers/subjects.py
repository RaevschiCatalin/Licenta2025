from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.postgres_setup import get_db
from models.database_models import Subject, User
from typing import List
from routers.auth import get_current_user
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("", response_model=List[dict])
async def get_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all available subjects.
    This endpoint is accessible by both teachers and admins.
    """
    try:
        # Check if user is authorized (teacher or admin)
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only teachers and admins can access subjects"
            )

        subjects = db.query(Subject).all()
        logger.info(f"Retrieved {len(subjects)} subjects for user {current_user.email}")
        return [{"id": subject.id, "name": subject.name} for subject in subjects]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving subjects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving subjects"
        ) 