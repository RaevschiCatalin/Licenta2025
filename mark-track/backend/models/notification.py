from typing import Optional
from pydantic import BaseModel

class MarkNotification(BaseModel):
    student_id: str
    teacher_id: str
    subject_id: str
    value: float
    description: Optional[str] = None
    is_read: bool = False

class AbsenceNotification(BaseModel):
    student_id: str
    teacher_id: str
    subject_id: str
    is_motivated: bool
    date: str
    description: Optional[str] = None
    is_read: bool = False

class ClassAsignmentNotification(BaseModel):
    pass

    