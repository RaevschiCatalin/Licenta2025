import os
from datetime import datetime, timedelta
import jwt

from dotenv import load_dotenv

from utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def create_jwt_token(email: str) -> str:
    print(SECRET_KEY)

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    print(token)
    return token
