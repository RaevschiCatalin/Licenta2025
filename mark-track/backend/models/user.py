from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    uid: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    email: EmailStr
class RegisterUserRequest(BaseModel):
    uid: str
    email: str

class AssignRoleRequest(BaseModel):
    uid: str
    code: str
