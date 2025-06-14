import re
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from sqlalchemy.orm import Session
from database.postgres_setup import get_db
from models.database_models import User, Student, Teacher, Admin
from utils.constants import TEACHER_CODE, STUDENT_CODE_PREFIX, ADMIN_CODE
import logging
import uuid
from models.auth import Token
from routers.auth import get_current_user
from datetime import timedelta
from utils.jwt_utils import create_access_token
from utils.jwt_utils import ACCESS_TOKEN_EXPIRE_MINUTES

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/assign-role", response_model=Token)
async def assign_role(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        data = await request.json()
        code = data.get('code', '')
        if not code:
            raise HTTPException(status_code=400, detail="Role code is required")
        user = db.query(User).filter(User.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.role != "pending":
            raise HTTPException(status_code=400, detail="Role already assigned")
        # Teacher role
        if code == TEACHER_CODE:
            teacher = Teacher(id=str(uuid.uuid4()), user_id=user.id)
            db.add(teacher)
            user.role = "teacher"
            user.status = "awaiting_details"
            db.commit()
            db.refresh(user)
            logger.info(f"Assigned teacher role to user {user.id}")
            # Issue new JWT with updated role and status
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.email, "role": user.role, "status": user.status.value},
                expires_delta=access_token_expires
            )
            # Set JWT as HttpOnly cookie
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,  # Always use secure cookies
                samesite="strict",  # Strict SameSite policy
                max_age=3600,
                path="/",
                domain="myapp.localhost"  # Match your domain
            )
            return {"access_token": access_token, "token_type": "bearer"}
        # Student role
        elif code.startswith(STUDENT_CODE_PREFIX):
            if not re.match(rf"^{STUDENT_CODE_PREFIX}\d{{4,5}}$", code):
                raise HTTPException(status_code=400, detail="Invalid student code format")
            existing_student = db.query(Student).filter(Student.student_id == code).first()
            if existing_student:
                raise HTTPException(status_code=400, detail="Student ID already exists")
            student = Student(id=str(uuid.uuid4()), user_id=user.id, student_id=code)
            db.add(student)
            user.role = "student"
            user.status = "awaiting_details"
            db.commit()
            db.refresh(user)
            logger.info(f"Assigned student role to user {user.id}")
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.email, "role": user.role, "status": user.status.value},
                expires_delta=access_token_expires
            )
            # Set JWT as HttpOnly cookie
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,  # Always use secure cookies
                samesite="strict",  # Strict SameSite policy
                max_age=3600,
                path="/",
                domain="myapp.localhost"  # Match your domain
            )
            return {"access_token": access_token, "token_type": "bearer"}
        # Admin role
        elif code == ADMIN_CODE:
            admin = Admin(id=str(uuid.uuid4()), user_id=user.id)
            db.add(admin)
            user.role = "admin"
            user.status = "active"
            db.commit()
            db.refresh(user)
            logger.info(f"Assigned admin role to user {user.id}")
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.email, "role": user.role, "status": user.status.value},
                expires_delta=access_token_expires
            )
            # Set JWT as HttpOnly cookie
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,  # Always use secure cookies
                samesite="strict",  # Strict SameSite policy
                max_age=3600,
                path="/",
                domain="myapp.localhost"  # Match your domain
            )
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=400, detail="Invalid role code")
    except Exception as e:
        logger.error(f"Error assigning role: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error assigning role: {str(e)}")

