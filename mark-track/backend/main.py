import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database.init_db import init_db
from database.postgres_setup import wait_for_db
from routers import auth, roles, profiles, subjects, admin, teacher, student, notifications
from middleware.rate_limit import limiter
from slowapi.middleware import SlowAPIMiddleware

#Logging    
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#DB Initialization
try:
    wait_for_db()
    init_db()
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    raise e

app = FastAPI(
    docs_url=None,  
    redoc_url=None,  
    openapi_url=None,  
)

api = FastAPI(
    docs_url=None,  
    redoc_url=None,  
    openapi_url=None,  
    redirect_slashes=False  
)

origins = os.getenv("ALLOWED_ORIGINS").split(",")

#CORS Middleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
    expose_headers=["Content-Type", "Authorization"],
    max_age=3600
)

#Rate Limit Middleware
api.state.limiter = limiter
api.add_middleware(SlowAPIMiddleware)

#Global Exception Handler
@api.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

#Include Routers
api.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api.include_router(roles.router, prefix="/roles", tags=["Roles"])
api.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
api.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
api.include_router(admin.router, prefix="/admin", tags=["Admin"])
api.include_router(teacher.router, prefix="/teacher", tags=["Teacher"])
api.include_router(student.router, prefix="/student", tags=["Student"])
api.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

#Root Route
@api.get("/")
async def root():
    return {"message": "Welcome to MarkTrack API"}

app.mount("/api", api)
