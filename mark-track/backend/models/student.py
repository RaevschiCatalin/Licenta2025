from pydantic import BaseModel
from typing import List


class StudentDetails(BaseModel):
    uid: str
    first_name: str
    last_name: str
    gov_number: str
    father_name: str


class StudentProfileRequest(BaseModel):
    first_name: str
    last_name: str
    father_name: str
    gov_number: str
    user_id: str


class AddStudentToClass(BaseModel):
    student_id: str

class StudentRequest(BaseModel):
    student_id: str

class AddStudentsToClass(BaseModel):
    student_ids: List[str]
