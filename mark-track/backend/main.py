import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database.init_db import init_db
from database.postgres_setup import wait_for_db
from routers import auth, roles, profiles, subjects, admin, teacher, student, notifications
from middleware.rate_limit import limiter
from slowapi.middleware import SlowAPIMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Wait for database to be ready
    wait_for_db()
    
    # Initialize database
    init_db()
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    raise e

# Create main app
app = FastAPI(
    docs_url=None,  # Disable Swagger UI
    redoc_url=None,  # Disable ReDoc
    openapi_url=None,  # Disable OpenAPI schema
)

# Create API sub-application
api = FastAPI(
    docs_url=None,  # Disable Swagger UI
    redoc_url=None,  # Disable ReDoc
    openapi_url=None,  # Disable OpenAPI schema
    redirect_slashes=False  # Disable automatic slash redirects
)

# Configure CORS
origins = [
    "https://myapp.localhost",
    "https://localhost",
    "https://127.0.0.1"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
    expose_headers=["Content-Type", "Authorization"],
    max_age=3600
)

# Add rate limit middleware
api.state.limiter = limiter
api.add_middleware(SlowAPIMiddleware)

# Global exception handler
@api.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Include routers in the API sub-application
api.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api.include_router(roles.router, prefix="/roles", tags=["Roles"])
api.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
api.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
api.include_router(admin.router, prefix="/admin", tags=["Admin"])
api.include_router(teacher.router, prefix="/teacher", tags=["Teacher"])
api.include_router(student.router, prefix="/student", tags=["Student"])
api.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

@api.get("/")
async def root():
    return {"message": "Welcome to MarkTrack API"}

# Mount the API sub-application under /api
app.mount("/api", api)
