from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, Request, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.postgres_setup import get_db
from models.database_models import User, Teacher, Student, Admin
from models.teacher import TeacherProfileRequest
from models.student import StudentProfileRequest
from models.auth import UserCreate, UserLogin, Token, UserResponse
from utils.security import verify_password, get_password_hash
from utils.jwt_utils import create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
from middleware.rate_limit import login_limit, register_limit
import uuid
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Get token from cookie
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    try:
        payload = verify_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/login", response_model=Token)
@login_limit
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint with rate limiting."""
    try:
        # Use parameterized query
        user = db.query(User).filter(User.email == form_data.username).first()
        
        if not user or not verify_password(form_data.password, user.password):
            logger.warning(f"Login failed: Invalid credentials for email {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role},
            expires_delta=access_token_expires
        )
        
        logger.info(f"Login successful for user {user.id}")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )

@router.post("/register", response_model=Token)
@register_limit
async def register_user(
    request: Request,
    user_data: UserCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    """Register new user and return JWT."""
    try:
        # Check if user exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user with hashed password
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            password=hashed_password,
            role=user_data.role,
            created_at=datetime.utcnow()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Create JWT
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": new_user.email, "role": new_user.role},
            expires_delta=access_token_expires
        )
        # Set JWT as HttpOnly cookie (for dev, secure=False)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production
            samesite="lax",
            max_age=3600,
            path="/"
        )
        logger.info(f"Successfully created user: {user_data.email}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    
    users = db.query(User).all()
    return users

@router.get("/user/{uid}", response_model=UserResponse)
async def get_user_by_id(
    uid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user by ID."""
    # Users can only access their own data unless they're admin
    if current_user.id != uid and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
