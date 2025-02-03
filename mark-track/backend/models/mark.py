from pydantic import BaseModel
from typing import Optional


class Mark(BaseModel):
    student_id: str
    teacher_id: str
    subject_id: str
    value: float
    description: Optional[str] = None
    date: Optional[str] = None

class UpdateMark(BaseModel):
    value: float
    description: Optional[str] = None
    date: Optional[str] = None