from pydantic import BaseModel


class LoginData(BaseModel):
    token: str