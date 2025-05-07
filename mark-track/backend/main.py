import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.init_db import init_db
from database.postgres_setup import wait_for_db
from routers import admin, auth, teacher, student

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from routers import auth, roles, profiles, subjects, admin, teacher, student, notifications

try:
    # Wait for database to be ready
    wait_for_db()
    
    # Initialize database
    init_db()
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    raise e

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(roles.router, prefix="/roles", tags=["Roles"])
app.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
app.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(teacher.router, prefix="/teacher", tags=["Teacher"])
app.include_router(student.router, prefix="/student", tags=["Student"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
async def root():
    return {"message": "Backend is working!"}
