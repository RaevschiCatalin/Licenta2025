from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TeacherDetails(BaseModel):
    uid: str
    first_name: str
    last_name: str
    father_name: str
    gov_number: str
    subject_id: str

class TeacherRequest(BaseModel):
    teacher_id: str

class MarkBase(BaseModel):
    student_id: str
    value: float = Field(..., ge=1, le=10)  
    subject_id: str
    date: datetime = Field(default_factory=datetime.now)

class MarkCreate(MarkBase):
    pass

class Mark(MarkBase):
    id: str
    teacher_id: str

class AbsenceBase(BaseModel):
    student_id: str
    subject_id: str
    date: datetime = Field(default_factory=datetime.now)
    is_motivated: bool = False

class AbsenceCreate(AbsenceBase):
    pass

class Absence(AbsenceBase):
    id: str
    teacher_id: str

class StudentStats(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    marks: List[Mark] = []
    absences: List[Absence] = []
    average_mark: float = 0
    total_absences: int = 0
    motivated_absences: int = 0

class ClassStats(BaseModel):
    class_id: str
    name: str
    average_mark: float = 0
    total_absences: int = 0
    motivated_absences: int = 0
    students: List[StudentStats] = []

class TeacherClass(BaseModel):
    id: str
    name: str
    subject_id: str

class TeacherClasses(BaseModel):
    classes: List[TeacherClass]

class StudentResponse(BaseModel):
    id: str
    student_id: str
    first_name: str
    last_name: str
    marks: Optional[List[Mark]] = None
    absences: Optional[List[Absence]] = None
    average_mark: Optional[float] = None
    total_absences: Optional[int] = None
    motivated_absences: Optional[int] = None

class StudentsResponse(BaseModel):
    students: List[StudentResponse]
