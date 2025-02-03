from pydantic import BaseModel

class CreateClassRequest(BaseModel):
    class_id: str

class AssignTeacherToClass(BaseModel):
    teacher_id: str