from pydantic import BaseModel
from typing import Optional


class Absence(BaseModel):
    student_id: str
    teacher_id: str
    subject_id: str
    is_motivated: bool
    description: Optional[str] = None
    date: Optional[str] = None

class UpdateAbsence(BaseModel):
    is_motivated: bool
    description: Optional[str] = None
    date: str = None