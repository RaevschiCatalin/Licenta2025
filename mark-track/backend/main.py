from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from firebase_admin import initialize_app


from routers import auth, roles, profiles, subjects, admin, teacher, student, notifications

try:
    initialize_app()
except ValueError:
    pass

app = FastAPI()


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
