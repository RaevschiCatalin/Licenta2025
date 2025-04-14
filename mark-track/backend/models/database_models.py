from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database.postgres_setup import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)  # Storing plaintext passwords
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    subject_id = Column(String, ForeignKey("subjects.id"))
    user_id = Column(String, ForeignKey("users.id"))
    
    user = relationship("User")
    subject = relationship("Subject")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(String, primary_key=True)
    student_id = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    user_id = Column(String, ForeignKey("users.id"))
    
    user = relationship("User")

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
    student_id = Column(String, ForeignKey("students.id"), primary_key=True)
    
    class_ = relationship("Class", back_populates="students")
    student = relationship("Student")

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

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
    
    student = relationship("Student")
    teacher = relationship("Teacher")
    subject = relationship("Subject")

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    
    user = relationship("User") 