from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Enum as SAEnum
from sqlalchemy.orm import relationship
from database.postgres_setup import Base
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
import enum

class RegistrationStatus(enum.Enum):
    incomplete = "incomplete"
    awaiting_details = "awaiting_details"
    active = "active"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Storing plaintext passwords
    role = Column(String, nullable=False)
    status = Column(SAEnum(RegistrationStatus), nullable=False, default=RegistrationStatus.incomplete)
    created_at = Column(DateTime, default=datetime.utcnow)
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    student = relationship("Student", back_populates="user", uselist=False)

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)
    gov_number = Column(String)
    subject_id = Column(String, ForeignKey("subjects.id"))
    user = relationship("User", back_populates="teacher")
    subject = relationship("Subject", back_populates="teachers")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)  # Added to support father_name in API
    gov_number = Column(String)
    student_id = Column(String, unique=True)
    user = relationship("User", back_populates="student")

class Class(Base):
    __tablename__ = "classes"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    students = relationship("ClassStudent", back_populates="class_")
    subjects = relationship("ClassSubject", back_populates="class_")

class ClassStudent(Base):
    __tablename__ = "class_students"
    
    class_id = Column(String, ForeignKey("classes.id"), primary_key=True)
    student_id = Column(String, ForeignKey("students.student_id"), primary_key=True)
    
    class_ = relationship("Class", back_populates="students")
    student = relationship("Student")

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    teachers = relationship("Teacher", back_populates="subject")
    classes = relationship("ClassSubject", back_populates="subject")

class ClassSubject(Base):
    __tablename__ = "class_subjects"
    
    class_id = Column(String, ForeignKey("classes.id"), primary_key=True)
    subject_id = Column(String, ForeignKey("subjects.id"), primary_key=True)
    teacher_id = Column(String, ForeignKey("teachers.id"))
    
    class_ = relationship("Class", back_populates="subjects")
    subject = relationship("Subject")
    teacher = relationship("Teacher")

class Mark(Base):
    __tablename__ = "marks"
    
    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("students.id"))
    teacher_id = Column(String, ForeignKey("teachers.id"))
    subject_id = Column(String, ForeignKey("subjects.id"))
    value = Column(Float)
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student")
    teacher = relationship("Teacher")
    subject = relationship("Subject")

class Absence(Base):
    __tablename__ = "absences"
    
    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("students.id"))
    teacher_id = Column(String, ForeignKey("teachers.id"))
    subject_id = Column(String, ForeignKey("subjects.id"))
    is_motivated = Column(Boolean, default=False)
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student")
    teacher = relationship("Teacher")
    subject = relationship("Subject")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("students.id"))
    teacher_id = Column(String, ForeignKey("teachers.id"))
    subject_id = Column(String, ForeignKey("subjects.id"))
    value = Column(Float, nullable=True)
    is_motivated = Column(Boolean, nullable=True)
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student")
    teacher = relationship("Teacher")
    subject = relationship("Subject")

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    
    user = relationship("User")

# Pydantic Models
class TeacherProfileBase(BaseModel):
    first_name: str
    last_name: str
    father_name: Optional[str] = None
    gov_number: Optional[str] = None
    subject_id: str

class TeacherProfileCreate(TeacherProfileBase):
    pass

class TeacherProfileUpdate(TeacherProfileBase):
    pass

class TeacherProfileResponse(TeacherProfileBase):
    id: str
    user_id: str
    email: str
    subject_name: Optional[str] = None

    class Config:
        from_attributes = True

class StudentProfileBase(BaseModel):
    first_name: str
    last_name: str
    father_name: Optional[str] = None
    gov_number: Optional[str] = None

class StudentProfileCreate(StudentProfileBase):
    pass

class StudentProfileUpdate(StudentProfileBase):
    pass

class StudentProfileResponse(StudentProfileBase):
    id: str
    user_id: str
    email: str
    student_id: str

    class Config:
        from_attributes = True 