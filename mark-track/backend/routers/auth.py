from datetime import datetime

from fastapi import APIRouter, HTTPException
from firebase_admin import auth

from database.firebase_setup import db
from models.login_data import LoginData
from models.user import RegisterUserRequest
from utils.jwt_utils import create_jwt_token
from utils.firebase_helpers import get_user_by_email

router = APIRouter()

@router.post("/login")
async def login(data: LoginData):
    try:
        if not isinstance(data.token, str):
            raise ValueError("The token must be a string.")
        decoded_token = auth.verify_id_token(data.token,clock_skew_seconds=60)
        email = decoded_token.get("email")

        if not email:
            raise HTTPException(status_code=400, detail="Email not found in token.")

        user = get_user_by_email(email)
        print(user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        role = user.get("role")
        uid = auth.get_user_by_email(email).uid
        jwt_token = create_jwt_token(email)
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "role": role,
            "uid": uid
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase token.")


@router.post("/register")
async def register_user(user_data: RegisterUserRequest):

    try:
        user_ref = db.collection("users").document(user_data.uid)
        user_ref.set({
            "email": user_data.email,
            "createdAt": datetime.utcnow(),
            "role": "pending"
        })
        return {"message": "User created successfully in Firestore."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")
