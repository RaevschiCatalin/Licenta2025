from pydantic import BaseModel

class Subject(BaseModel):
    subject_id: str
    teacher_id: str

class SubjectName(BaseModel):
    subject_name: str
