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

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Add rate limit middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
)

# Include routers
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
    return {"message": "Welcome to MarkTrack API"}
